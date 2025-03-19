import tkinter as tk
from tkinter import messagebox
import random
import threading
import time
import speech_recognition as sr
import sys
import platform

class BaseballNameGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Baseball Name Game")
        self.root.geometry("400x500")
        
        # Check microphone access on startup
        self.check_microphone_access()
        
        # List of MLB players
        self.mlb_players = list(set([
            # Current Braves (2024)
            "Ronald Acuna Jr", "Matt Olson", "Austin Riley", "Ozzie Albies",
            "Michael Harris II", "Sean Murphy", "Orlando Arcia", "Marcell Ozuna",
            "Spencer Strider", "Max Fried", "Charlie Morton", "Chris Sale",
            "Raisel Iglesias", "A.J. Minter", "Pierce Johnson", "Jarred Kelenic",
            "Travis d'Arnaud", "Adam Duvall", "Forrest Wall", "Aaron Bummer",
            
            # Braves Legends and Hall of Famers
            "Hank Aaron", "Chipper Jones", "Greg Maddux", "Tom Glavine",
            "John Smoltz", "Dale Murphy", "Phil Niekro", "Warren Spahn",
            "Eddie Mathews", "Kid Nichols", "Rabbit Maranville", "Joe Torre",
            "Andruw Jones", "Fred McGriff", "David Justice", "Bob Horner",
            
            # 2021 World Series Champions
            "Freddie Freeman", "Ozzie Albies", "Austin Riley", "Dansby Swanson",
            "Eddie Rosario", "Adam Duvall", "Jorge Soler", "Travis d'Arnaud",
            "Max Fried", "Charlie Morton", "Ian Anderson", "Will Smith",
            "Tyler Matzek", "Luke Jackson", "A.J. Minter", "Jesse Chavez",
            
            # 1995 World Series Champions
            "Chipper Jones", "Fred McGriff", "David Justice", "Marquis Grissom",
            "Javy Lopez", "Ryan Klesko", "Mark Lemke", "Jeff Blauser",
            "Greg Maddux", "Tom Glavine", "John Smoltz", "Steve Avery",
            "Mark Wohlers", "Alejandro Pena", "Pedro Borbon", "Luis Polonia",
            
            # 1990s Braves Dynasty
            "Terry Pendleton", "Otis Nixon", "Rafael Belliard", "Damon Berryhill",
            "Ron Gant", "Deion Sanders", "Sid Bream", "Francisco Cabrera",
            
            # Milwaukee/Boston Braves
            "Johnny Sain", "Tommy Holmes", "Bob Elliott", "Earl Torgeson",
            "Al Dark", "Jim Russell", "Sibby Sisti", "Dick Culler", "Mort Cooper",
            "Joe Adcock", "Del Crandall", "Johnny Logan", "Bill Bruton", 
            "Lew Burdette", "Bob Buhl", "Frank Torre", "Wes Covington",
            
            # Current Nationals (2024)
            "CJ Abrams", "Lane Thomas", "Joey Meneses", "Keibert Ruiz",
            "Luis Garcia", "Jesse Winker", "James Wood", "Riley Adams",
            "Josiah Gray", "MacKenzie Gore", "Patrick Corbin", "Trevor Williams",
            "Kyle Finnegan", "Hunter Harvey", "Jordan Weems", "Stone Garrett",
            "Victor Robles", "Jake Alu", "Dominic Smith", "Nick Senzel",
            
            # Nationals/Expos Legends
            "Gary Carter", "Andre Dawson", "Tim Raines", "Vladimir Guerrero",
            "Pedro Martinez", "Larry Walker", "Tim Wallach", "Dennis Martinez",
            "Steve Rogers", "Ellis Valentine", "Warren Cromartie", "Rusty Staub",
            "Ryan Zimmerman", "Max Scherzer", "Stephen Strasburg", "Bryce Harper",
            "Anthony Rendon", "Juan Soto", "Trea Turner", "Jordan Zimmermann",
            
            # 2019 World Series Champions
            "Anthony Rendon", "Trea Turner", "Adam Eaton", "Howie Kendrick",
            "Ryan Zimmerman", "Victor Robles", "Kurt Suzuki", "Yan Gomes",
            "Max Scherzer", "Stephen Strasburg", "Patrick Corbin", "Anibal Sanchez",
            "Sean Doolittle", "Daniel Hudson", "Fernando Rodney", "Matt Adams",
            
            # Early Nationals
            "Alfonso Soriano", "Nick Johnson", "Chad Cordero", "Livan Hernandez",
            "John Patterson", "Brad Wilkerson", "Jose Guillen", "Cristian Guzman",
            "Jose Vidro", "John Lannan", "Austin Kearns", "Felipe Lopez",
            
            # Current Rays (2024)
            "Randy Arozarena", "Yandy Diaz", "Isaac Paredes", "Josh Lowe",
            "Brandon Lowe", "Jose Siri", "Harold Ramirez", "Taylor Walls",
            "Zach Eflin", "Tyler Glasnow", "Pete Fairbanks", "Jason Adam",
            "Christian Bethancourt", "Junior Caminero", "Curtis Mead", "Amed Rosario",
            "Ryan Thompson", "Colin Poche", "Shawn Armstrong", "Manuel Margot",
            
            # Rays Legends and Stars
            "Evan Longoria", "Carl Crawford", "Ben Zobrist", "David Price",
            "James Shields", "Scott Kazmir", "Carlos Pena", "B.J. Upton",
            "Fred McGriff", "Wade Boggs", "Aubrey Huff", "Rocco Baldelli",
            
            # 2008 American League Champions
            "Evan Longoria", "Carl Crawford", "B.J. Upton", "Carlos Pena",
            "Akinori Iwamura", "Dioner Navarro", "Jason Bartlett", "Cliff Floyd",
            "Scott Kazmir", "Matt Garza", "Andy Sonnanstine", "Grant Balfour",
            "Dan Wheeler", "J.P. Howell", "Edwin Jackson", "Troy Percival",
            
            # Devil Rays Era
            "Wade Boggs", "Fred McGriff", "Jose Canseco", "Greg Vaughn",
            "Quinton McCracken", "Miguel Cairo", "Bobby Smith", "Dave Martinez",
            "Wilson Alvarez", "Roberto Hernandez", "Rolando Arrojo", "Bryan Rekar",
            
            # Current White Sox (2024)
            "Luis Robert Jr", "Eloy Jimenez", "Andrew Benintendi", "Yoan Moncada",
            "Andrew Vaughn", "Michael Kopech", "Dylan Cease", "Garrett Crochet",
            "Dominic Fletcher", "Paul DeJong", "Kevin Pillar", "Nicky Lopez",
            "Michael Soroka", "Chris Flexen", "John Brebbia", "Tim Hill",
            "Tanner Banks", "Lane Ramsey", "Korey Lee", "Zach Remillard",
            
            # White Sox Legends
            "Frank Thomas", "Luke Appling", "Nellie Fox", "Luis Aparicio",
            "Carlton Fisk", "Harold Baines", "Paul Konerko", "Mark Buehrle",
            "Billy Pierce", "Minnie Minoso", "Eddie Collins", "Red Faber",
            "Ted Lyons", "Ray Schalk", "Ed Walsh", "Joe Jackson",
            
            # 2005 World Series Champions
            "Paul Konerko", "Jermaine Dye", "Scott Podsednik", "Joe Crede",
            "Aaron Rowand", "Juan Uribe", "A.J. Pierzynski", "Carl Everett",
            "Mark Buehrle", "Jose Contreras", "Jon Garland", "Freddy Garcia",
            "Bobby Jenks", "Neal Cotts", "Cliff Politte", "Dustin Hermanson",
            
            # Historical White Sox
            "Dick Allen", "Bill Melton", "Jorge Orta", "Chet Lemon",
            "Ralph Garr", "Richie Zisk", "Eric Soderholm", "Brian Downing",
            "Wilbur Wood", "Goose Gossage", "Terry Forster", "Bart Johnson",
            "Ron Kittle", "Greg Walker", "Ozzie Guillen", "Richard Dotson",
            "LaMarr Hoyt", "Floyd Bannister", "Tom Seaver", "Steve Carlton",
            
            # Current Blue Jays (2024)
            "Vladimir Guerrero Jr", "Bo Bichette", "George Springer", "Kevin Kiermaier",
            "Justin Turner", "Daulton Varsho", "Alejandro Kirk", "Davis Schneider",
            "Jose Berrios", "Chris Bassitt", "Kevin Gausman", "Jordan Romano",
            "Yusei Kikuchi", "Erik Swanson", "Genesis Cabrera", "Cavan Biggio",
            "Danny Jansen", "Isiah Kiner-Falefa", "Santiago Espinal", "Nathan Lukes",
            
            # Blue Jays Legends
            "Roberto Alomar", "Roy Halladay", "Dave Stieb", "Tony Fernandez",
            "Carlos Delgado", "Joe Carter", "George Bell", "Vernon Wells",
            "Jimmy Key", "Pat Hentgen", "John Olerud", "Lloyd Moseby",
            "Jesse Barfield", "Tom Henke", "Duane Ward", "Devon White",
            
            # 1992-1993 World Series Champions
            "Roberto Alomar", "Joe Carter", "John Olerud", "Paul Molitor",
            "Devon White", "Pat Borders", "Tony Fernandez", "Dave Winfield",
            "Juan Guzman", "Jack Morris", "Dave Stewart", "Pat Hentgen",
            "Todd Stottlemyre", "Duane Ward", "Tom Henke", "Jimmy Key",
            
            # Historical Blue Jays
            "Roy Howell", "Otto Velez", "Rick Bosetti", "John Mayberry",
            "Doug Ault", "Dave McKay", "Alan Ashby", "Bob Bailor",
            "Jerry Garvin", "Jim Clancy", "Tom Underwood", "Pete Vuckovich",
            
            # Current Angels (2024)
            "Mike Trout", "Anthony Rendon", "Taylor Ward", "Logan O'Hoppe",
            "Luis Rengifo", "Zach Neto", "Mickey Moniak", "Brandon Drury",
            "Patrick Sandoval", "Reid Detmers", "Tyler Anderson", "Griffin Canning",
            "Carlos Estevez", "Jose Soriano", "Robert Stephenson", "Matt Moore",
            "Jo Adell", "Nolan Schanuel", "Jose Suarez", "Chase Silseth",
            
            # Angels Legends
            "Nolan Ryan", "Rod Carew", "Reggie Jackson", "Vladimir Guerrero",
            "Tim Salmon", "Jim Fregosi", "Bobby Grich", "Chuck Finley",
            "Brian Downing", "Garret Anderson", "Jim Edmonds", "Troy Percival",
            "Don Baylor", "Frank Tanana", "Mike Witt", "Bob Boone",
            
            # 2002 World Series Champions
            "Troy Glaus", "Garret Anderson", "Tim Salmon", "Darin Erstad",
            "David Eckstein", "Scott Spiezio", "Adam Kennedy", "Bengie Molina",
            "Troy Percival", "John Lackey", "Jarrod Washburn", "Francisco Rodriguez",
            "Brad Fullmer", "Brendan Donnelly", "Ben Weber", "Kevin Appier",
            
            # Historical Angels
            "Alex Johnson", "Andy Messersmith", "Frank Tanana", "Bobby Valentine",
            "Don Baylor", "Rick Miller", "Dave Chalk", "Jerry Remy",
            "Rudy May", "Ken McMullen", "Doug DeCinces", "Brian Downing",
            "Bob Boone", "Mike Witt", "Dick Schofield", "Wally Joyner",
            
            # Current Orioles (2024)
            "Adley Rutschman", "Gunnar Henderson", "Cedric Mullins", "Anthony Santander",
            "Ryan Mountcastle", "Jordan Westburg", "Colton Cowser", "Jackson Holliday",
            "Corbin Burnes", "Grayson Rodriguez", "John Means", "Dean Kremer",
            "Felix Bautista", "Danny Coulombe", "Yennier Cano", "Craig Kimbrel",
            "James McCann", "Ramon Urias", "Ryan O'Hearn", "Kyle Bradish",
            
            # Orioles Legends
            "Cal Ripken Jr", "Brooks Robinson", "Frank Robinson", "Eddie Murray",
            "Jim Palmer", "Earl Weaver", "Mike Mussina", "Paul Blair",
            "Boog Powell", "Mark Belanger", "Dave McNally", "Ken Singleton",
            "Brady Anderson", "Mike Flanagan", "Rick Dempsey", "Al Bumbry",
            
            # 1983 World Series Champions
            "Cal Ripken Jr", "Eddie Murray", "Ken Singleton", "Al Bumbry",
            "Rick Dempsey", "John Lowenstein", "Gary Roenicke", "Rich Dauer",
            "Jim Palmer", "Scott McGregor", "Mike Boddicker", "Storm Davis",
            "Tippy Martinez", "Mike Flanagan", "Dan Ford", "Todd Cruz",
            
            # Historical Orioles
            "Frank Robinson", "Brooks Robinson", "Boog Powell", "Paul Blair",
            "Dave Johnson", "Mark Belanger", "Don Buford", "Elrod Hendricks",
            "Jim Palmer", "Dave McNally", "Mike Cuellar", "Pete Richert",
            "Rafael Palmeiro", "Roberto Alomar", "Brady Anderson", "Mike Mussina",
            
            # Current Cubs (2024)
            "Dansby Swanson", "Seiya Suzuki", "Ian Happ", "Christopher Morel",
            "Cody Bellinger", "Nico Hoerner", "Justin Steele", "Kyle Hendricks",
            "Jameson Taillon", "Drew Smyly", "Adbert Alzolay", "Julian Merryweather",
            "Michael Busch", "Nick Madrigal", "Patrick Wisdom", "Mike Tauchman",
            "Yan Gomes", "Alexander Canario", "Pete Crow-Armstrong", "Jordan Wicks",
            
            # Cubs Legends
            "Ernie Banks", "Ron Santo", "Billy Williams", "Ryne Sandberg",
            "Fergie Jenkins", "Greg Maddux", "Andre Dawson", "Cap Anson",
            "Hack Wilson", "Gabby Hartnett", "Billy Herman", "Stan Hack",
            "Phil Cavarretta", "Rick Reuschel", "Bruce Sutter", "Lee Smith",
            
            # 2016 World Series Champions
            "Kris Bryant", "Anthony Rizzo", "Javier Baez", "Ben Zobrist",
            "Kyle Schwarber", "Dexter Fowler", "Addison Russell", "Jason Heyward",
            "Jon Lester", "Jake Arrieta", "Kyle Hendricks", "John Lackey",
            "Aroldis Chapman", "Pedro Strop", "Carl Edwards Jr", "Mike Montgomery",
            
            # Historical Cubs
            "Sammy Sosa", "Kerry Wood", "Mark Prior", "Aramis Ramirez",
            "Derrek Lee", "Moises Alou", "Carlos Zambrano", "Ryan Dempster",
            "Mark Grace", "Shawon Dunston", "Rick Wilkins", "Jerome Walton",
            "Bill Madlock", "Rick Monday", "Jose Cardenal", "Bill Buckner",
            
            # Current Astros (2024)
            "Jose Altuve", "Alex Bregman", "Yordan Alvarez", "Kyle Tucker",
            "Jose Abreu", "Jeremy Pena", "Chas McCormick", "Yainer Diaz",
            "Framber Valdez", "Justin Verlander", "Cristian Javier", "Jose Urquidy",
            "Josh Hader", "Ryan Pressly", "Bryan Abreu", "Rafael Montero",
            "Mauricio Dubon", "Jake Meyers", "Victor Caratini", "Hunter Brown",
            
            # Astros Legends
            "Jeff Bagwell", "Craig Biggio", "Nolan Ryan", "Jose Cruz",
            "Jimmy Wynn", "Larry Dierker", "Joe Morgan", "Cesar Cedeno",
            "Mike Scott", "J.R. Richard", "Don Wilson", "Bob Watson",
            "Joe Niekro", "Billy Wagner", "Roy Oswalt", "Lance Berkman",
            
            # 2017 World Series Champions
            "Jose Altuve", "Carlos Correa", "George Springer", "Alex Bregman",
            "Yuli Gurriel", "Josh Reddick", "Marwin Gonzalez", "Brian McCann",
            "Justin Verlander", "Dallas Keuchel", "Lance McCullers Jr", "Charlie Morton",
            "Ken Giles", "Chris Devenski", "Joe Musgrove", "Brad Peacock",
            
            # Historical Astros
            "Lance Berkman", "Roy Oswalt", "Jeff Kent", "Carlos Lee",
            "Hunter Pence", "Michael Bourn", "Wandy Rodriguez", "Brad Lidge",
            "Morgan Ensberg", "Adam Everett", "Brad Ausmus", "Jose Valverde",
            
            # Current Pirates (2024)
            "Oneil Cruz", "Ke'Bryan Hayes", "Bryan Reynolds", "Andrew McCutchen",
            "Jack Suwinski", "Connor Joe", "Henry Davis", "Michael A. Taylor",
            "Mitch Keller", "Marco Gonzales", "Martin Perez", "David Bednar",
            "Aroldis Chapman", "Edward Olivares", "Rowdy Tellez", "Jared Jones",
            "Paul Skenes", "Roansy Contreras", "Luis Ortiz", "Carmen Mlodzinski",
            
            # Pirates Legends
            "Roberto Clemente", "Honus Wagner", "Willie Stargell", "Ralph Kiner",
            "Bill Mazeroski", "Paul Waner", "Lloyd Waner", "Pie Traynor",
            "Max Carey", "Arky Vaughan", "Fred Clarke", "Jake Beckley",
            "Dave Parker", "Barry Bonds", "Andy Van Slyke", "Doug Drabek",
            
            # 1979 World Series Champions
            "Willie Stargell", "Dave Parker", "Bill Madlock", "Phil Garner",
            "Omar Moreno", "John Candelaria", "Kent Tekulve", "Tim Foli",
            "Ed Ott", "Bill Robinson", "Mike Easler", "Don Robinson",
            "Jim Rooker", "Bruce Kison", "Grant Jackson", "Steve Nicosia",
            
            # Historical Pirates
            "Barry Bonds", "Andy Van Slyke", "Bobby Bonilla", "Jay Bell",
            "Jeff King", "Orlando Merced", "Don Slaught", "Mike LaValliere",
            "Doug Drabek", "John Smiley", "Bob Walk", "Stan Belinda",
            
            # Current Cardinals (2024)
            "Paul Goldschmidt", "Nolan Arenado", "Willson Contreras", "Brendan Donovan",
            "Lars Nootbaar", "Jordan Walker", "Masyn Winn", "Tommy Edman",
            "Sonny Gray", "Miles Mikolas", "Kyle Gibson", "Steven Matz",
            "Ryan Helsley", "Giovanny Gallegos", "JoJo Romero", "Andrew Knizner",
            "Dylan Carlson", "Alec Burleson", "Victor Scott II", "Zack Thompson",
            
            # Cardinals Legends
            "Stan Musial", "Bob Gibson", "Lou Brock", "Rogers Hornsby",
            "Ozzie Smith", "Albert Pujols", "Red Schoendienst", "Enos Slaughter",
            "Johnny Mize", "Dizzy Dean", "Joe Medwick", "Ken Boyer",
            "Curt Flood", "Jim Bottomley", "Jesse Haines", "Frankie Frisch",
            
            # 2011 World Series Champions
            "Albert Pujols", "Yadier Molina", "Matt Holliday", "Lance Berkman",
            "David Freese", "Jon Jay", "Rafael Furcal", "Skip Schumaker",
            "Chris Carpenter", "Kyle Lohse", "Jaime Garcia", "Jake Westbrook",
            "Jason Motte", "Fernando Salas", "Marc Rzepczynski", "Allen Craig",
            
            # Historical Cardinals
            "Lou Brock", "Bob Gibson", "Curt Flood", "Tim McCarver",
            "Julian Javier", "Mike Shannon", "Dal Maxvill", "Ted Simmons",
            "Joe Torre", "Keith Hernandez", "Garry Templeton", "Ken Reitz",
            
            # Current Phillies (2024)
            "Trea Turner", "Bryce Harper", "Kyle Schwarber", "J.T. Realmuto",
            "Alec Bohm", "Brandon Marsh", "Bryson Stott", "Nick Castellanos",
            "Zack Wheeler", "Aaron Nola", "Ranger Suarez", "Taijuan Walker",
            "Jose Alvarado", "Gregory Soto", "Matt Strahm", "Jeff Hoffman",
            "Johan Rojas", "Edmundo Sosa", "Garrett Stubbs", "Spencer Turnbull",
            
            # Phillies Legends
            "Mike Schmidt", "Steve Carlton", "Robin Roberts", "Richie Ashburn",
            "Chuck Klein", "Jim Bunning", "Dick Allen", "Pete Rose",
            "Larry Bowa", "Greg Luzinski", "Garry Maddox", "Bob Boone",
            "Tony Taylor", "Chris Short", "Johnny Callison", "Del Ennis",
            
            # 2008 World Series Champions
            "Jimmy Rollins", "Chase Utley", "Ryan Howard", "Pat Burrell",
            "Shane Victorino", "Jayson Werth", "Pedro Feliz", "Carlos Ruiz",
            "Cole Hamels", "Brett Myers", "Jamie Moyer", "Joe Blanton",
            "Brad Lidge", "Ryan Madson", "J.C. Romero", "Chad Durbin",
            
            # Historical Phillies
            "Curt Schilling", "Scott Rolen", "Bobby Abreu", "Mike Lieberthal",
            "Doug Glanville", "Rico Brogna", "Ricky Bottalico", "Mickey Morandini",
            "Von Hayes", "Juan Samuel", "Steve Bedrosian", "Darren Daulton",
            
            # Current Rockies (2024)
            "Kris Bryant", "Ryan McMahon", "Ezequiel Tovar", "Nolan Jones",
            "Charlie Blackmon", "Brendan Rodgers", "Elias Diaz", "Brenton Doyle",
            "Kyle Freeland", "Cal Quantrill", "Dakota Hudson", "Daniel Bard",
            "Justin Lawrence", "Tyler Kinley", "Jake Bird", "Peter Lambert",
            "Michael Toglia", "Sean Bouchard", "Elehuris Montero", "Austin Gomber",
            
            # Rockies Legends
            "Todd Helton", "Larry Walker", "Troy Tulowitzki", "Carlos Gonzalez",
            "Nolan Arenado", "Vinny Castilla", "Dante Bichette", "Andres Galarraga",
            "DJ LeMahieu", "Matt Holliday", "Ellis Burks", "Jeff Francis",
            "Aaron Cook", "Ubaldo Jimenez", "Jorge De La Rosa", "Huston Street",
            
            # 2007 World Series Team
            "Matt Holliday", "Todd Helton", "Troy Tulowitzki", "Garrett Atkins",
            "Brad Hawpe", "Kaz Matsui", "Yorvit Torrealba", "Willy Taveras",
            "Jeff Francis", "Aaron Cook", "Josh Fogg", "Ubaldo Jimenez",
            "Brian Fuentes", "Manny Corpas", "LaTroy Hawkins", "Ryan Spilborghs",
            
            # Historical Rockies
            "Dante Bichette", "Larry Walker", "Andres Galarraga", "Vinny Castilla",
            "Ellis Burks", "Walt Weiss", "Eric Young", "Joe Girardi",
            "Armando Reynoso", "Marvin Freeman", "David Nied", "Bruce Ruffin"
        ]))  # Properly closing the list(set([...]))

        # Initialize game state
        self.score = 0
        self.current_player = ""
        self.required_letter = ""
        self.is_listening = False
        self.timer_active = False
        self.clock_active = False
        self.time_left = 10  # 10 seconds per turn
        
        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Baseball Name Game", font=("Arial", 16))
        self.title_label.pack(pady=10)

        self.instructions_label = tk.Label(self.root, text="Press Start to begin", font=("Arial", 12))
        self.instructions_label.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, font=("Arial", 12))
        self.start_button.pack(pady=5)

        self.player_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.player_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.rules_button = tk.Button(self.root, text="Show Rules", command=self.show_rules, font=("Arial", 12))
        self.rules_button.pack(pady=5)

        self.clock_label = tk.Label(self.root, text="Time: 10", font=("Arial", 14))
        self.clock_label.pack(pady=5)

    def show_rules(self):
        rules_text = """
        Baseball Name Game Rules:

        1. The game starts by showing you a baseball player's name
        2. You must say a player whose FIRST NAME starts with the 
           first letter of the LAST NAME of the previous player
        3. You have 10 seconds to give each answer
        4. The clock resets to 10 seconds after each correct answer
        5. Game ends when the time runs out
        
        Example:
        If the game shows "Mookie Betts"
        - You need to say a player whose first name starts with 'B'
        - If you say "Bobby Witt Jr", that's correct!
        - Then you need a player whose first name starts with 'W'
        - And so on...

        Tips:
        - Speak clearly into your microphone
        - Watch the clock - you have 10 seconds per turn
        - Your score increases with each correct answer
        
        Ready to play? Click 'Start Game' to begin!
        """
        messagebox.showinfo("Game Rules", rules_text)

    def start_game(self):
        # Show rules when starting the first game
        if self.score == 0:
            self.show_rules()
        
        self.current_player = random.choice(self.mlb_players)
        self.required_letter = self.current_player.split()[-1][0]
        self.player_label.config(text=f"Current Player: {self.current_player}")
        self.instructions_label.config(text=f"Say a player whose first name starts with '{self.required_letter}'!")
        
        # Start continuous listening
        self.is_listening = True
        self.clock_active = True
        self.time_left = 10
        
        # Start the game clock and continuous listening in separate threads
        threading.Thread(target=self.run_game_clock, daemon=True).start()
        threading.Thread(target=self.continuous_listen, daemon=True).start()

    def run_game_clock(self):
        while self.clock_active and self.time_left > 0:
            self.clock_label.config(text=f"Time: {self.time_left}")
            time.sleep(1)
            self.time_left -= 1
            
        if self.time_left <= 0:
            self.clock_active = False
            self.is_listening = False
            self.instructions_label.config(text="Time's up! Game Over!")
            messagebox.showinfo("Game Over", f"Game Over! Final Score: {self.score}")
            self.score = 0
            self.score_label.config(text="Score: 0")

    def speak_name(self):
        if self.timer_active:
            return
        
        try:
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
        except Exception as e:
            messagebox.showerror("Error", "Could not access microphone. Please check your settings.")
            return

        self.result_label.config(text="")
        self.is_listening = True
        self.timer_active = True
        
        threading.Thread(target=self.listen_for_name, daemon=True).start()
        threading.Thread(target=self.start_timer, daemon=True).start()

    def start_timer(self):
        for i in range(5, 0, -1):
            if not self.timer_active:
                break
            self.instructions_label.config(text=f"Time left: {i} seconds")
            time.sleep(1)
        
        self.timer_active = False
        if self.is_listening:
            self.is_listening = False
            self.instructions_label.config(text="Time's up! Try again")

    def listen_for_name(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.instructions_label.config(text="Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=4)
                text = recognizer.recognize_google(audio)
                
                spoken_name = text.strip().title()
                self.result_label.config(text=f"You said: {spoken_name}", fg="blue")
                
                # Check if the first letter of the FIRST name matches the required letter
                spoken_first_name = spoken_name.split()[0]
                if spoken_first_name[0].lower() == self.required_letter.lower():
                    self.score += 1
                    self.score_label.config(text=f"Score: {self.score}")
                    self.result_label.config(text=f"Correct! {spoken_name}", fg="green")
                    
                    # Get the first letter of the spoken player's last name
                    last_name_letter = spoken_name.split()[-1][0]
                    
                    # Find a valid player whose first name starts with that letter
                    valid_players = [p for p in self.mlb_players 
                                   if p.split()[0][0].lower() == last_name_letter.lower() 
                                   and p != spoken_name]
                    
                    if valid_players:
                        self.current_player = random.choice(valid_players)
                        self.required_letter = self.current_player.split()[-1][0]
                        self.player_label.config(text=f"Next Player: {self.current_player}")
                        self.instructions_label.config(text=f"Say a player whose first name starts with '{self.required_letter}'!")
                    else:
                        # If no valid players found, end the game with a win
                        self.clock_active = False
                        messagebox.showinfo("Congratulations!", 
                                          f"No more valid players available! You win!\nFinal Score: {self.score}")
                        self.start_game()  # Restart the game
                        return
                    
                    # Reset the clock after correct answer
                    self.time_left = 10
                    return
                        
                self.result_label.config(text=f"Invalid name. First name must start with '{self.required_letter}': {spoken_name}", fg="red")
                
        except sr.UnknownValueError:
            self.result_label.config(text="Could not understand audio", fg="red")
        except sr.RequestError:
            self.result_label.config(text="Could not reach Google Speech Recognition service", fg="red")
        except Exception as e:
            self.result_label.config(text=f"Error occurred while listening: {str(e)}", fg="red")
        
        self.is_listening = False
        self.timer_active = False

    def continuous_listen(self):
        if not hasattr(self, 'recognizer'):
            self.recognizer = sr.Recognizer()
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_adjustment_ratio = 1.5
            
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                while self.is_listening and self.clock_active:
                    try:
                        self.instructions_label.config(text=f"Listening... Say a name starting with '{self.required_letter}'")
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                        
                        try:
                            text = self.recognizer.recognize_google(audio)
                            if not text.strip():
                                continue
                                
                            spoken_name = text.strip().title()
                            self.result_label.config(text=f"You said: {spoken_name}", fg="blue")
                            
                            # Check if the first letter of the FIRST name matches the required letter
                            spoken_first_name = spoken_name.split()[0]
                            if spoken_first_name[0].lower() == self.required_letter.lower():
                                self.score += 1
                                self.score_label.config(text=f"Score: {self.score}")
                                self.result_label.config(text=f"Correct! {spoken_name}", fg="green")
                                
                                # Get the first letter of the spoken player's last name
                                last_name_letter = spoken_name.split()[-1][0]
                                
                                # Find a valid player whose first name starts with that letter
                                valid_players = [p for p in self.mlb_players 
                                               if p.split()[0][0].lower() == last_name_letter.lower() 
                                               and p != spoken_name]
                                
                                if valid_players:
                                    self.current_player = random.choice(valid_players)
                                    self.required_letter = self.current_player.split()[-1][0]
                                    self.player_label.config(text=f"Next Player: {self.current_player}")
                                    self.instructions_label.config(text=f"Say a player whose first name starts with '{self.required_letter}'!")
                                    # Reset the clock to 10 seconds after correct answer
                                    self.time_left = 10
                                else:
                                    # If no valid players found, end the game with a win
                                    self.clock_active = False
                                    self.is_listening = False
                                    messagebox.showinfo("Congratulations!", 
                                                      f"No more valid players available! You win!\nFinal Score: {self.score}")
                                    self.start_game()  # Restart the game
                                    return
                            else:
                                self.result_label.config(text=f"Invalid name. First name must start with '{self.required_letter}': {spoken_name}", fg="red")
                                
                        except sr.UnknownValueError:
                            pass  # Ignore unrecognized speech
                        except sr.RequestError:
                            self.result_label.config(text="Could not reach speech recognition service", fg="red")
                            
                    except sr.WaitTimeoutError:
                        pass  # Continue listening if timeout
                    
        except Exception as e:
            self.result_label.config(text=f"Error with microphone: {str(e)}", fg="red")
            self.is_listening = False
            self.clock_active = False

    def check_microphone_access(self):
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    if retry_count == 0:
                        messagebox.showinfo("Microphone Setup", 
                            "The game needs microphone access to work.\n\n" +
                            "1. Make sure your microphone is connected\n" +
                            "2. Allow microphone access if prompted\n" +
                            "3. Speak clearly when playing")
                    
                    # Adjust the recognizer sensitivity to ambient noise
                    self.instructions_label.config(text="Calibrating microphone...")
                    recognizer.dynamic_energy_threshold = True
                    recognizer.energy_threshold = 4000
                    recognizer.dynamic_energy_adjustment_ratio = 1.5
                    recognizer.adjust_for_ambient_noise(source, duration=2)
                    
                    # Test microphone with quick audio capture
                    self.instructions_label.config(text="Testing microphone...")
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=1)
                    
                    messagebox.showinfo("Success", 
                        "Microphone is working!\n\n" +
                        "You can now start the game.")
                    self.instructions_label.config(text="Press Start to begin")
                    return True
                    
            except sr.RequestError:
                messagebox.showerror("Connection Error", 
                    "Could not access speech recognition service.\n" +
                    "Please check your internet connection.")
                return False
                
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    if platform.system() == 'Darwin':  # macOS
                        messagebox.showerror("Microphone Error",
                            "Could not access microphone.\n\n" +
                            "Please follow these steps:\n\n" +
                            "1. Click on Apple menu ()\n" +
                            "2. Select System Settings\n" +
                            "3. Click Privacy & Security\n" +
                            "4. Click Microphone\n" +
                            "5. Enable access for Terminal and Python\n" +
                            "6. Restart the game after enabling access")
                    else:
                        messagebox.showerror("Microphone Error",
                            "Could not access microphone.\n\n" +
                            "Please check:\n" +
                            "1. Microphone is properly connected\n" +
                            "2. Microphone permissions are enabled\n" +
                            "3. No other app is using the microphone")
                    return False
                else:
                    response = messagebox.askretrycancel("Microphone Error",
                        f"Attempt {retry_count} of {max_retries}: Could not access microphone.\n\n" +
                        "Would you like to try again?")
                    if not response:
                        return False
                    time.sleep(1)  # Wait before retrying

if __name__ == "__main__":
    root = tk.Tk()
    app = BaseballNameGame(root)
    root.mainloop() 