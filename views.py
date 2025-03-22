from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import random
import json
import speech_recognition as sr
import time

# List of MLB players (current Braves players for 2024)
MLB_PLAYERS = [
    # Current Braves (2024)
    "Ronald Acuña Jr.", "Matt Olson", "Austin Riley", "Ozzie Albies",
    "Marcell Ozuna", "Michael Harris II", "Orlando Arcia", "Travis d'Arnaud",
    "Sean Murphy", "Max Fried", "Spencer Strider", "Charlie Morton",
    "Bryce Elder", "Reynaldo López", "A.J. Minter", "Raisel Iglesias",
    "Joe Jiménez", "Pierce Johnson", "Aaron Bummer", "Dylan Lee",
    
    # Braves Legends
    "Hank Aaron", "Chipper Jones", "Greg Maddux", "Tom Glavine",
    "John Smoltz", "Dale Murphy", "Phil Niekro", "Warren Spahn",
    "Eddie Mathews", "Andruw Jones", "David Justice", "Fred McGriff",
    "Terry Pendleton", "Javy López", "Andrelton Simmons", "Craig Kimbrel",
    "Freddie Freeman", "Dansby Swanson", "Ronald Acuña Sr.", "Brian McCann",
    
    # Current MLB Stars
    "Shohei Ohtani", "Mike Trout", "Mookie Betts", "Aaron Judge",
    "Juan Soto", "Fernando Tatis Jr.", "Vladimir Guerrero Jr.", "Rafael Devers",
    "Corey Seager", "Trea Turner", "Pete Alonso", "Francisco Lindor",
    "Jose Ramirez", "Yordan Alvarez", "Kyle Tucker", "Julio Rodriguez",
    "Adley Rutschman", "Gunnar Henderson", "Evan Carter", "Jackson Holliday",
    
    # MLB Legends
    "Babe Ruth", "Willie Mays", "Ted Williams", "Mickey Mantle",
    "Jackie Robinson", "Roberto Clemente", "Stan Musial", "Joe DiMaggio",
    "Ty Cobb", "Walter Johnson", "Cy Young", "Lou Gehrig",
    "Yogi Berra", "Sandy Koufax", "Bob Gibson", "Nolan Ryan",
    "Cal Ripken Jr.", "Tony Gwynn", "Ken Griffey Jr.", "Derek Jeter",
    
    # Modern Era Greats
    "Barry Bonds", "Ken Griffey Jr.", "Greg Maddux", "Randy Johnson",
    "Pedro Martinez", "Mariano Rivera", "Derek Jeter", "Albert Pujols",
    "Mike Trout", "Clayton Kershaw", "Max Scherzer", "Justin Verlander",
    "Miguel Cabrera", "Ichiro Suzuki", "David Ortiz", "Alex Rodriguez",
    "Manny Ramirez", "Roger Clemens", "Barry Larkin", "Ken Griffey Sr.",
    
    # International Stars
    "Ichiro Suzuki", "Hideki Matsui", "Shohei Ohtani", "Yu Darvish",
    "Masahiro Tanaka", "Yasiel Puig", "Jose Abreu", "Yoenis Cespedes",
    "Vladimir Guerrero", "Roberto Alomar", "Mariano Rivera", "Pedro Martinez",
    "David Ortiz", "Manny Ramirez", "Albert Pujols", "Miguel Cabrera",
    "Carlos Correa", "Francisco Lindor", "Jose Ramirez", "Ronald Acuña Jr.",
    
    # Rookies and Prospects
    "Evan Carter", "Jackson Holliday", "Wyatt Langford", "Paul Skenes",
    "Max Clark", "Walker Jenkins", "Jacob Berry", "Brooks Lee",
    "Colson Montgomery", "Jordan Lawlar", "Marcel Mayer", "Jackson Jobe",
    "Cade Horton", "Kyle Manzardo", "Colt Keith", "Jasson Dominguez",
    "Eury Perez", "Evan Carter", "Wyatt Langford", "Jackson Holliday",
    
    # All-Time Greats
    "Babe Ruth", "Willie Mays", "Ted Williams", "Mickey Mantle",
    "Jackie Robinson", "Roberto Clemente", "Stan Musial", "Joe DiMaggio",
    "Ty Cobb", "Walter Johnson", "Cy Young", "Lou Gehrig",
    "Yogi Berra", "Sandy Koufax", "Bob Gibson", "Nolan Ryan",
    "Cal Ripken Jr.", "Tony Gwynn", "Ken Griffey Jr.", "Derek Jeter",
    
    # Hall of Famers
    "Hank Aaron", "Willie Mays", "Ted Williams", "Mickey Mantle",
    "Jackie Robinson", "Roberto Clemente", "Stan Musial", "Joe DiMaggio",
    "Ty Cobb", "Walter Johnson", "Cy Young", "Lou Gehrig",
    "Yogi Berra", "Sandy Koufax", "Bob Gibson", "Nolan Ryan",
    "Cal Ripken Jr.", "Tony Gwynn", "Ken Griffey Jr.", "Derek Jeter",
    
    # World Series MVPs
    "Babe Ruth", "Willie Mays", "Sandy Koufax", "Bob Gibson",
    "Reggie Jackson", "Pete Rose", "Derek Jeter", "David Ortiz",
    "Madison Bumgarner", "Stephen Strasburg", "Corey Seager", "Jeremy Peña",
    "Randy Johnson", "Curt Schilling", "Josh Beckett", "Cole Hamels",
    "David Freese", "Pablo Sandoval", "George Springer", "Steve Pearce"
]

class GameState:
    def __init__(self):
        self.current_player = None
        self.score = 0
        self.time_left = 60
        self.is_running = False
        self.recognizer = sr.Recognizer()

game_state = GameState()

def index(request):
    return render(request, 'game/index.html')

@require_http_methods(["GET"])
def start_game(request):
    game_state.current_player = random.choice(MLB_PLAYERS)
    game_state.score = 0
    game_state.time_left = 60
    game_state.is_running = True
    return JsonResponse({
        'current_player': game_state.current_player,
        'score': game_state.score,
        'time_left': game_state.time_left
    })

@csrf_exempt
@require_http_methods(["POST"])
def check_answer(request):
    try:
        data = json.loads(request.body)
        answer = data.get('answer', '').strip()
        is_speech = data.get('is_speech', False)
        
        if not answer:
            return JsonResponse({
                'correct': False,
                'message': 'Please provide an answer'
            }, status=400)
        
        # Case-insensitive comparison
        is_correct = answer.lower() == game_state.current_player.lower()
        
        if is_correct:
            game_state.score += 1
            game_state.current_player = random.choice(MLB_PLAYERS)
        
        return JsonResponse({
            'correct': is_correct,
            'score': game_state.score,
            'current_player': game_state.current_player,
            'spoken_name': answer if is_speech else None
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'correct': False,
            'message': 'Invalid JSON data'
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def start_speech_recognition(request):
    try:
        with sr.Microphone() as source:
            game_state.recognizer.adjust_for_ambient_noise(source)
            audio = game_state.recognizer.listen(source)
            
            try:
                spoken_name = game_state.recognizer.recognize_google(audio)
                return JsonResponse({
                    'success': True,
                    'spoken_name': spoken_name
                })
            except sr.UnknownValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Could not understand audio'
                }, status=400)
            except sr.RequestError:
                return JsonResponse({
                    'success': False,
                    'message': 'Could not request results'
                }, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@require_http_methods(["GET"])
def get_state(request):
    return JsonResponse({
        'current_player': game_state.current_player,
        'score': game_state.score,
        'time_left': game_state.time_left,
        'is_running': game_state.is_running
    })