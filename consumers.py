import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .views import MLB_PLAYERS, game_state
import asyncio
from vosk import Model, KaldiRecognizer
import wave
import numpy as np
import io

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.model = Model("model")
        self.rec = KaldiRecognizer(self.model, 16000)
        self.audio_buffer = []
        print("WebSocket connection established")
        
    async def disconnect(self, close_code):
        print(f"WebSocket connection closed with code: {close_code}")
        
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            print(f"Received message type: {data.get('type')}")
            
            if data['type'] == 'start_game':
                # Start a new game
                game_state.reset()
                await self.send(json.dumps({
                    'type': 'game_state',
                    'current_player': game_state.current_player,
                    'required_letter': game_state.required_letter
                }))
                print("Game started")
                
            elif data['type'] == 'audio_data':
                # Process audio data
                audio_data = np.array(data['audio'], dtype=np.float32)
                self.audio_buffer.extend(audio_data)
                
                # Process audio in chunks of 2 seconds
                if len(self.audio_buffer) >= 32000:  # 2 seconds at 16kHz
                    audio_chunk = self.audio_buffer[:32000]
                    self.audio_buffer = self.audio_buffer[32000:]
                    
                    # Convert to WAV format for Vosk using in-memory buffer
                    wav_data = self.float32_to_wav(audio_chunk)
                    
                    # Process with Vosk
                    if self.rec.AcceptWaveform(wav_data):
                        result = json.loads(self.rec.Result())
                        if result.get('text'):
                            print(f"Recognized text: {result['text']}")
                            # Check the answer
                            is_correct = game_state.check_answer(result['text'])
                            await self.send(json.dumps({
                                'type': 'answer_result',
                                'correct': is_correct,
                                'message': 'Correct!' if is_correct else 'Incorrect. Try again!'
                            }))
                            
                            if is_correct:
                                await self.send(json.dumps({
                                    'type': 'game_state',
                                    'current_player': game_state.current_player,
                                    'required_letter': game_state.required_letter
                                }))
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            await self.send(json.dumps({
                'type': 'error',
                'message': 'Error processing audio. Please try again.'
            }))
    
    def float32_to_wav(self, audio_data):
        # Convert float32 to 16-bit PCM
        audio_data = np.clip(audio_data * 32768, -32768, 32767).astype(np.int16)
        
        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(audio_data.tobytes())
        
        # Get the WAV data from the buffer
        wav_buffer.seek(0)
        return wav_buffer.read() 