import os
import sys
import logging
import json
import traceback
from typing import Dict, Any
from pathlib import Path

from dotenv import load_dotenv
from colorama import init, Fore, Style, just_fix_windows_console

# Load environment variables from .env file
load_dotenv()

# Fix Windows console for color output
just_fix_windows_console()

# Check Python version
if sys.version_info < (3, 7):
    print("Error: Python 3.7 or higher is required.")
    sys.exit(1)

# Initialize colorama for colored console output
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Import after environment is loaded
from speech_handler import SpeechHandler
from location_service import LocationService
from whatsapp_sender import WhatsAppSender

class BinoEmergencyAssistant:
    def __init__(self, config_path: str = 'config.json'):
        """Initialize the Bino Emergency Assistant."""
        self.config_path = config_path
        self.config = self._load_config(config_path)
        
        # Initialize services with error handling
        try:
            self.location_service = LocationService()
            self.whatsapp_sender = WhatsAppSender(config_path)
            
            # Initialize speech handler with wake word and emergency phrases
            self.speech_handler = SpeechHandler(
                wake_word="bino",
                emergency_phrases=["i'm in danger", "help me", "emergency", "i need help"]
            )
            
            self._show_welcome_message()
            
        except Exception as e:
            print(f"\n{Fore.RED}Error initializing Bino Emergency Assistant: {e}\n")
            if "No module named 'pyaudio'" in str(e):
                print(f"{Fore.YELLOW}Please install PyAudio using the following command:")
                print("pip install pipwin")
                print("pipwin install pyaudio")
            traceback.print_exc()
            sys.exit(1)
    
    def _show_welcome_message(self):
        """Display the welcome message and instructions."""
        print(Fore.CYAN + "=" * 60)
        print("BINO EMERGENCY ASSISTANT".center(60))
        print("=" * 60 + Style.RESET_ALL)
        print("\n" + Fore.YELLOW + "Important:" + Style.RESET_ALL)
        print("1. Make sure you're logged in to WhatsApp Web")
        print("2. Ensure your microphone is working properly")
        print("3. Keep the application running in the background")
        print("4. Speak clearly when prompted")
        print("\n" + Fore.GREEN + "System ready. Say 'Bino' to start." + Style.RESET_ALL)
    
    def _load_config(self, config_path: str) -> dict:
        """
        Load configuration from both JSON file and environment variables.
        Environment variables take precedence over the config file.
        """
        config = {}
        
        # First, load from config file if it exists
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            logging.warning(f"Could not load config file: {e}. Using environment variables only.")
        
        # Then override with environment variables if they exist
        env_config = {
            'trusted_contact': os.getenv('TRUSTED_CONTACT'),
            'user_name': os.getenv('USER_NAME', 'User'),
            'emergency_message': os.getenv('EMERGENCY_MESSAGE', '🚨 I need help!'),
            'whatsapp_token': os.getenv('WHATSAPP_TOKEN'),
            'whatsapp_phone_number_id': os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        }
        
        # Update config with environment variables, skipping None values
        for key, value in env_config.items():
            if value is not None:
                config[key] = value
        
        # Validate required fields
        required_fields = ['trusted_contact', 'whatsapp_token', 'whatsapp_phone_number_id']
        missing_fields = [field for field in required_fields if not config.get(field)]
        
        if missing_fields:
            logging.error(f"Missing required configuration: {', '.join(missing_fields)}")
            if 'whatsapp_token' in missing_fields or 'whatsapp_phone_number_id' in missing_fields:
                print(f"\n{Fore.RED}Error: WhatsApp API credentials are missing.{Style.RESET_ALL}")
                print("Please set the following environment variables:")
                print("- WHATSAPP_TOKEN")
                print("- WHATSAPP_PHONE_NUMBER_ID")
                print("\nOr add them to your config.json file.")
                print(f"See {Fore.CYAN}.env.example{Style.RESET_ALL} for an example configuration.")
                sys.exit(1)
        
        return config
    
    def handle_emergency(self):
        """Handle emergency situation by getting location and sending alert."""
        print(Fore.RED + "\nEMERGENCY DETECTED!" + Style.RESET_ALL)
        print("Getting your location...")
        
        # Get current location
        location = self.location_service.get_current_location()
        
        if location:
            print(f"\n{Fore.GREEN}Location found!{Style.RESET_ALL}")
            print(f"Address: {location.get('address')}")
            print(f"Map: {location.get('maps_link')}")
            
            # Send alert via WhatsApp
            print("\nSending emergency alert...")
            if self.whatsapp_sender.send_emergency_alert(location):
                print(Fore.GREEN + "Alert sent successfully!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Failed to send alert. Please check your internet connection." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Could not determine your location. Please check your internet connection." + Style.RESET_ALL)
    
    def start(self):
        """Start the Bino Emergency Assistant."""
        try:
            self.speech_handler.start_listening(self.handle_emergency)
        except KeyboardInterrupt:
            print("\n" + Fore.YELLOW + "Shutting down Bino Emergency Assistant..." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"\nAn error occurred: {e}" + Style.RESET_ALL)
            logging.error(f"Error in main loop: {e}")

if __name__ == "__main__":
    try:
        assistant = BinoEmergencyAssistant()
        assistant.start()
    except Exception as e:
        print(Fore.RED + f"\nFatal error: {e}" + Style.RESET_ALL)
        logging.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
