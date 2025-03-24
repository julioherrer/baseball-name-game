from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import random
import json
import speech_recognition as sr
import time
import os
import subprocess
import platform
import webbrowser
from datetime import datetime

# List of MLB players
MLB_PLAYERS = list(set([
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
    "Hunter Pence", "Michael Bourn", "Wandy Rodriguez", "Brad Lidge"
]))

class GameState:
    def __init__(self):
        self.score = 0
        self.current_player = ""
        self.required_letter = ""
        self.is_listening = False
        self.time_left = 10
        self.recognizer = sr.Recognizer()
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_adjustment_ratio = 1.5

    def get_next_player(self, spoken_name):
        # Get the first letter of the spoken player's last name
        last_name_letter = spoken_name.split()[-1][0]
        
        # Find a valid player whose first name starts with that letter
        valid_players = [p for p in MLB_PLAYERS 
                        if p.split()[0][0].lower() == last_name_letter.lower() 
                        and p != spoken_name]
        
        if valid_players:
            self.current_player = random.choice(valid_players)
            self.required_letter = self.current_player.split()[-1][0]
            return True
        return False

# Global game state
game_state = GameState()

def index(request):
    return render(request, 'game/index.html', {
        'high_scores': []  # We'll implement high scores later
    })

@require_http_methods(["GET"])
def start_game(request):
    try:
        # Reset game state
        game_state.score = 0
        game_state.current_player = random.choice(MLB_PLAYERS)
        game_state.required_letter = game_state.current_player.split()[-1][0]
        game_state.time_left = 10
        game_state.is_listening = False
        
        # Initialize speech recognizer
        game_state.recognizer = sr.Recognizer()
        game_state.recognizer.dynamic_energy_threshold = True
        game_state.recognizer.energy_threshold = 3000
        game_state.recognizer.dynamic_energy_adjustment_ratio = 1.5
        
        return JsonResponse({
            'current_player': game_state.current_player,
            'required_letter': game_state.required_letter,
            'score': game_state.score,
            'time_left': game_state.time_left
        })
    except Exception as e:
        print(f"Error starting game: {str(e)}")
        return JsonResponse({
            'error': 'Failed to start game',
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def check_answer(request):
    data = json.loads(request.body)
    spoken_name = data.get('answer', '').strip().title()
    
    # Check if the first letter of the FIRST name matches the required letter
    spoken_first_name = spoken_name.split()[0]
    if spoken_first_name[0].lower() == game_state.required_letter.lower():
        game_state.score += 1
        
        if game_state.get_next_player(spoken_name):
            return JsonResponse({
                'correct': True,
                'current_player': game_state.current_player,
                'required_letter': game_state.required_letter,
                'score': game_state.score,
                'time_left': 10,  # Reset timer on correct answer
                'message': f"Correct! {spoken_name}"
            })
        else:
            return JsonResponse({
                'correct': True,
                'game_over': True,
                'win': True,
                'score': game_state.score,
                'message': "No more valid players available! You win!"
            })
    
    return JsonResponse({
        'correct': False,
        'message': f"Invalid name. First name must start with '{game_state.required_letter}': {spoken_name}"
    })

@csrf_exempt
@require_http_methods(["POST"])
def start_speech(request):
    """Start speech recognition and return the recognized text"""
    try:
        # First check if microphone is available
        try:
            with sr.Microphone() as source:
                pass
        except Exception as e:
            print(f"Microphone check failed: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Microphone not available. Please check your microphone settings and permissions.'
            })

        r = sr.Recognizer()
        with sr.Microphone() as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=1.0)
            # Set energy threshold for better recognition
            r.energy_threshold = 3000  # Lowered threshold for better sensitivity
            # Set pause threshold to be more responsive
            r.pause_threshold = 0.5  # Reduced pause threshold
            # Set dynamic energy threshold
            r.dynamic_energy_threshold = True
            # Set dynamic energy adjustment ratio
            r.dynamic_energy_adjustment_ratio = 1.5
            
            print("Listening...")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                print("Processing...")
                
                try:
                    text = r.recognize_google(audio)
                    print(f"Recognized text: {text}")
                    return JsonResponse({
                        'success': True,
                        'spoken_name': text.strip().title()
                    })
                except sr.UnknownValueError:
                    print("Could not understand audio")
                    return JsonResponse({
                        'success': False,
                        'message': 'Could not understand audio. Please speak more clearly.'
                    })
                except sr.RequestError as e:
                    print(f"Could not request results; {str(e)}")
                    return JsonResponse({
                        'success': False,
                        'message': 'Could not reach speech recognition service. Please check your internet connection.'
                    })
            except sr.WaitTimeoutError:
                print("No speech detected within timeout")
                return JsonResponse({
                    'success': False,
                    'message': 'No speech detected. Please try speaking again.'
                })
    except Exception as e:
        print(f"Error in speech recognition: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'Error accessing microphone: {str(e)}'
        })

@require_http_methods(["GET"])
def show_rules(request):
    rules_text = """Baseball Name Game Rules:

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

Ready to play? Click 'Start Game' to begin!"""
    
    return JsonResponse({'rules': rules_text})

@require_http_methods(["GET"])
def check_microphone(request):
    try:
        with sr.Microphone() as source:
            game_state.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            return JsonResponse({'available': True})
    except:
        return JsonResponse({'available': False})

def get_state(request):
    """Return the current game state"""
    return JsonResponse({
        'current_player': game_state.current_player,
        'required_letter': game_state.required_letter,
        'score': game_state.score,
        'time_left': game_state.time_left
    })

def save_score(request):
    """Save the current score"""
    if request.method == 'POST':
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
    return JsonResponse({'error': 'Invalid request method'})