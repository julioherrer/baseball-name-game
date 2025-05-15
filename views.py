from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import random
import json
import os
import logging
import azure.cognitiveservices.speech as speechsdk
import threading
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of MLB players
MLB_PLAYERS = [
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
    
    # Boston Red Sox - Current and All-Time Greats
    "Rafael Devers", "Trevor Story", "Jarren Duran", "Triston Casas", "Masataka Yoshida",
    "Tyler O'Neill", "Connor Wong", "Reese McGuire", "Enmanuel Valdez", "Ceddanne Rafaela",
    "Wilyer Abreu", "Vaughn Grissom", "Bobby Dalbec", "Garrett Whitlock", "Brayan Bello",
    "Kutter Crawford", "Nick Pivetta", "Tanner Houck", "Josh Winckowski", "Kenley Jansen",
    "Chris Martin", "Brennan Bernardino", "Justin Slaten", "Joely Rodriguez", "Zack Kelly",
    # All-time greats
    "Ted Williams", "Carl Yastrzemski", "David Ortiz", "Pedro Martinez", "Jim Rice",
    "Wade Boggs", "Dustin Pedroia", "Mookie Betts", "Nomar Garciaparra", "Roger Clemens",
    "Jason Varitek", "Johnny Damon", "Manny Ramirez", "Dwight Evans", "Luis Tiant",
    "Tim Wakefield", "Curt Schilling", "Bill Lee", "Rico Petrocelli", "Mo Vaughn",
    "Jimmie Foxx", "Bobby Doerr", "Dom DiMaggio", "Carlton Fisk", "Tony Conigliaro",
    "Jackie Bradley Jr.", "Mike Lowell", "Kevin Youkilis", "Shane Victorino", "Koji Uehara",
    "Keith Foulke", "Jon Lester", "Clay Buchholz", "Rich Gedman", "Ellis Burks",
    "Trot Nixon", "Bill Mueller", "John Valentin", "Reggie Smith", "Frank Malzone",
    "George Scott", "Harry Hooper", "Mel Parnell", "Joe Cronin", "Dick Radatz",
    "Jim Lonborg", "Fred Lynn", "Rick Burleson", "Tom Brunansky", "Dave Henderson",
    "Mike Greenwell", "Butch Hobson", "Steve Crawford", "Bob Stanley", "Bill Monbouquette",
    "Gene Conley", "Marty Barrett", "Jerry Remy", "Rick Wise", "Dennis Eckersley",
    "Ellis Kinder", "Johnny Pesky", "Vern Stephens", "Tex Hughson", "Joe Dobson",
    "Boo Ferriss", "Denny Galehouse", "Sam Horn", "Billy Goodman", "Pinky Higgins",
    "Herb Pennock", "Everett Scott", "Chick Stahl", "Tris Speaker", "Babe Ruth",
    "Smoky Joe Wood", "Dutch Leonard", "Ray Collins", "Larry Gardner", "Duffy Lewis",
    "Heinie Wagner", "Bill Carrigan", "Jake Stahl", "Harry Lord", "Buck Freeman",
    "Jimmy Collins", "Cy Young"
]

class GameState:
    def __init__(self):
        self.current_player = None
        self.score = 0
        self.time_left = 10
        self.is_running = False
        self.required_letter = ""
        self.timer_thread = None
        self.lock = threading.Lock()
        self.used_players = set()  # Track used players to avoid repetition
        self.is_listening = False
        self.game_phase = "waiting"
        self.feedback_message = ""
        self.last_spoken_name = ""

    def reset(self):
        with self.lock:
            try:
                # Get a random player that hasn't been used
                available_players = [p for p in MLB_PLAYERS if p not in self.used_players]
                if not available_players:
                    available_players = MLB_PLAYERS  # Reset if all players used
                    self.used_players.clear()
                
                self.current_player = random.choice(available_players)
                self.used_players.add(self.current_player)
                self.score = 0
                self.time_left = 10
                self.is_running = True
                self.is_listening = False
                self.game_phase = "playing"
                self.feedback_message = ""
                self.last_spoken_name = ""
                
                # Get the last letter of the player's last name
                self.required_letter = self.current_player.split()[-1][-1].lower()
                
                # Stop any existing timer thread
                if self.timer_thread and self.timer_thread.is_alive():
                    self.is_running = False
                    self.timer_thread.join(timeout=1.0)
                
                # Start new timer thread
                self.timer_thread = threading.Thread(target=self.run_timer)
                self.timer_thread.daemon = True
                self.timer_thread.start()
                
            except Exception as e:
                logger.error(f"Error in game state reset: {str(e)}")
                raise

    def run_timer(self):
        while self.is_running and self.time_left > 0:
            time.sleep(1)
            with self.lock:
                self.time_left -= 1
                if self.time_left <= 0:
                    self.is_running = False
                    break

# Create a global game state instance
game_state = GameState()

def index(request):
    return render(request, 'game/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def start_game(request):
    try:
        # Reset the game state
        game_state.reset()
        
        # Ensure the game state is properly initialized
        if not game_state.current_player or not game_state.required_letter:
            logger.error("Game state not properly initialized")
            return JsonResponse({
                'success': False,
                'message': 'Failed to initialize game state'
            }, status=500)
            
        return JsonResponse({
            'success': True,
            'player': game_state.current_player,
            'score': game_state.score,
            'time_left': game_state.time_left,
            'required_letter': game_state.required_letter,
            'message': f"Say a player whose first name starts with '{game_state.required_letter}'"
        })
    except Exception as e:
        logger.error(f"Error starting game: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Failed to start game'
        }, status=500)

@require_http_methods(["GET"])
def timer(request):
    try:
        with game_state.lock:
            return JsonResponse({
                'success': True,
                'time_left': game_state.time_left,
                'is_running': game_state.is_running
            })
    except Exception as e:
        logger.error(f"Error getting timer state: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Failed to get timer state'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def start_recognition(request):
    """Start speech recognition using Azure."""
    try:
        if game_state.is_listening:
            return JsonResponse({
                'success': False,
                'error': 'Already listening'
            })

        if not game_state.is_running:
            return JsonResponse({
                'success': False,
                'error': 'Game is not running'
            })

        game_state.is_listening = True
        game_state.game_phase = "listening"
        game_state.feedback_message = "Listening..."
        
        # Create speech configuration
        speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv('AZURE_SPEECH_KEY'),
            region=os.getenv('AZURE_SPEECH_REGION')
        )
        speech_config.speech_recognition_language = "en-US"

        # Create audio configuration
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, 
            audio_config=audio_config
        )
        
        # Start recognition
        result = speech_recognizer.recognize_once_async().get()
        game_state.is_listening = False
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            game_state.recognized_text = result.text.strip()
            game_state.game_phase = "checking"
            game_state.feedback_message = "Checking your answer..."
            return JsonResponse({
                'success': True,
                'text': game_state.recognized_text,
                'phase': game_state.game_phase,
                'message': game_state.feedback_message
            })
        else:
            game_state.game_phase = "speaking"
            game_state.feedback_message = f"No speech detected. Try again! Say a player whose first name starts with '{game_state.required_letter}'"
            return JsonResponse({
                'success': False,
                'error': 'No speech detected',
                'phase': game_state.game_phase,
                'message': game_state.feedback_message
            })
            
    except Exception as e:
        game_state.is_listening = False
        game_state.game_phase = "speaking"
        game_state.feedback_message = f"Error: {str(e)}. Try again!"
        logger.error(f"Error in speech recognition: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'phase': game_state.game_phase,
            'message': game_state.feedback_message
        })

@csrf_exempt
@require_http_methods(["POST"])
def check_answer(request):
    """Check if the player's answer is valid."""
    if not game_state.is_running:
        return JsonResponse({
            'success': False,
            'message': 'Game is not running',
            'game_over': True
        })

    try:
        data = json.loads(request.body)
        answer = data.get('answer', '').strip().title()
        
        # Check if the answer is a valid MLB player
        if answer not in MLB_PLAYERS:
            return JsonResponse({
                'success': False,
                'message': f"'{answer}' is not a valid MLB player. Try again!",
                'player': game_state.current_player,
                'required_letter': game_state.required_letter
            })

        # Check if the player has already been used
        if answer in game_state.used_players:
            return JsonResponse({
                'success': False,
                'message': f"'{answer}' has already been used. Try another player!",
                'player': game_state.current_player,
                'required_letter': game_state.required_letter
            })

        # Check if the first letter of the answer matches the required letter
        if answer[0].lower() != game_state.required_letter:
            return JsonResponse({
                'success': False,
                'message': f"Player name must start with '{game_state.required_letter}'. Try again!",
                'player': game_state.current_player,
                'required_letter': game_state.required_letter
            })

        # Answer is correct
        game_state.score += 1
        game_state.used_players.add(answer)
        
        # Get the last letter of the answered player's last name
        last_letter = answer.split()[-1][-1].lower()
        
        # Find a valid next player
        valid_players = [p for p in MLB_PLAYERS 
                        if p not in game_state.used_players 
                        and p.split()[0][0].lower() == last_letter]
        
        if valid_players:
            game_state.current_player = random.choice(valid_players)
            game_state.used_players.add(game_state.current_player)
            game_state.required_letter = game_state.current_player.split()[-1][-1].lower()
            
            return JsonResponse({
                'success': True,
                'correct': True,
                'player': game_state.current_player,
                'score': game_state.score,
                'required_letter': game_state.required_letter,
                'message': f"Correct! Now say a player whose first name starts with '{game_state.required_letter}'"
            })
        else:
            # No more valid players
            game_state.is_running = False
            return JsonResponse({
                'success': True,
                'correct': True,
                'message': f"Congratulations! No more valid players available! You win with {game_state.score} points!",
                'score': game_state.score,
                'game_over': True
            })
            
    except Exception as e:
        logger.error(f"Error checking answer: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Error checking answer. Please try again.'
        }, status=500)

@require_http_methods(["GET"])
def get_state(request):
    """Get the current game state."""
    return JsonResponse({
        'success': True,
        'player': game_state.current_player,
        'time_left': game_state.time_left,
        'score': game_state.score,
        'required_letter': game_state.required_letter,
        'is_running': game_state.is_running,
        'phase': game_state.game_phase,
        'message': game_state.feedback_message,
        'last_spoken_name': game_state.last_spoken_name
    })

@require_http_methods(["GET"])
def show_rules(request):
    """Show the game rules."""
    return JsonResponse({
        'success': True,
        'rules': [
            'Say the name of an MLB player when prompted',
            'The player\'s name must start with the last letter of the previous player\'s name',
            'You have 30 seconds to name as many players as possible',
            'Each correct answer adds 1 point to your score',
            'The game ends when you run out of time or can\'t think of another valid player'
        ]
    })

@csrf_exempt
@require_http_methods(["POST"])
def save_score(request):
    try:
        data = json.loads(request.body)
        score = data.get('score', 0)
        player_name = data.get('player_name', 'Anonymous')
        
        # Load existing scores
        scores = []
        if os.path.exists('high_scores.json'):
            with open('high_scores.json', 'r') as f:
                scores = json.load(f)
        
        # Add new score
        scores.append({'name': player_name, 'score': score})
        
        # Sort scores and keep top 5
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:5]
        
        # Save scores
        with open('high_scores.json', 'w') as f:
            json.dump(scores, f)
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)})