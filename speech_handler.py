import speech_recognition as sr
import time
import logging
import sys
from typing import Optional, Callable, List

class SpeechHandler:
    def __init__(self, wake_word: str = "bino", emergency_phrases: List[str] = None):
        self.recognizer = sr.Recognizer()
        self.wake_word = wake_word.lower()
        self.emergency_phrases = emergency_phrases or ["i'm in danger", "help me", "emergency"]
        self.is_listening = False
        
        # List available microphones
        try:
            self.available_mics = sr.Microphone.list_microphone_names()
            print("\nAvailable audio input devices:")
            for i, mic in enumerate(self.available_mics):
                print(f"{i}: {mic}")
            
            # Try to use the default microphone first
            self.microphone = sr.Microphone()
            print("\nUsing default microphone.")
            
            # Adjust for ambient noise with a longer timeout
            with self.microphone as source:
                print("Adjusting for ambient noise, please wait...")
                self.recognizer.adjust_for_ambient_noise(source, duration=3)
                
        except OSError as e:
            print(f"\nError initializing microphone: {e}")
            print("Please check your audio input devices and try again.")
            sys.exit(1)
    
    def listen_for_wake_word(self, timeout: int = 5) -> bool:
        """
        Listen for the wake word.
        
        Args:
            timeout: Time in seconds to wait for the wake word
            
        Returns:
            bool: True if wake word detected, False otherwise
        """
        print(f"Say '{self.wake_word}' to start...")
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=3)
                
            # Recognize speech using Google's speech recognition
            text = self.recognizer.recognize_google(audio).lower()
            print(f"Heard: {text}")
            
            if self.wake_word in text:
                print("Wake word detected!")
                return True
                
        except sr.WaitTimeoutError:
            print("Listening timed out. Waiting for wake word...")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            
        return False
    
    def listen_for_emergency(self, timeout: int = 5) -> bool:
        """
        Listen for emergency phrases after wake word is detected.
        
        Args:
            timeout: Time in seconds to wait for a response
            
        Returns:
            bool: True if emergency phrase detected or timeout reached, False otherwise
        """
        print("Listening for emergency phrase... (say 'I'm in danger' or stay silent for 5 seconds)")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)
                
            # Try to recognize the speech
            text = self.recognizer.recognize_google(audio).lower()
            print(f"Heard: {text}")
            
            # Check for emergency phrases
            if any(phrase in text for phrase in self.emergency_phrases):
                print("Emergency phrase detected!")
                return True
                
        except sr.WaitTimeoutError:
            print("No speech detected. Treating as emergency due to silence.")
            return True
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            
        return False
    
    def start_listening(self, emergency_callback: Callable):
        """
        Start continuously listening for the wake word and emergency phrases.
        
        Args:
            emergency_callback: Function to call when an emergency is detected
        """
        self.is_listening = True
        print("Bino Emergency System is now active.")
        
        while self.is_listening:
            try:
                if self.listen_for_wake_word():
                    if self.listen_for_emergency():
                        emergency_callback()
                        # Wait a bit before listening again
                        time.sleep(5)
            except KeyboardInterrupt:
                print("\nStopping Bino Emergency System...")
                self.is_listening = False
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(2)  # Prevent tight loop on errors

if __name__ == "__main__":
    def test_emergency():
        print("EMERGENCY DETECTED!")
    
    handler = SpeechHandler()
    handler.start_listening(test_emergency)
