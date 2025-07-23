import json
import logging
import os
from datetime import datetime
from typing import Dict, Optional
import requests

class WhatsAppSender:
    def __init__(self, config_path: str = 'config.json'):
        self.config = self._load_config(config_path)
        self.base_url = "https://graph.facebook.com/v19.0/"
        self.headers = {
            'Authorization': f"Bearer {self.config.get('whatsapp_token', '')}",
            'Content-Type': 'application/json'
        }

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            return {}

    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send a WhatsApp message using the WhatsApp Business API.
        
        Args:
            to_number: Recipient's phone number with country code (e.g., "1234567890")
            message: The message to send
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        phone_number_id = self.config.get("whatsapp_phone_number_id")
        if not phone_number_id:
            logging.error("WhatsApp phone number ID not configured.")
            return False

        # Format the phone number correctly (remove any non-digit characters except +)
        to_number = ''.join(c for c in to_number if c.isdigit() or c == '+')
        if not to_number.startswith('+'):
            to_number = f"+{to_number}"

        url = f"{self.base_url}{phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_number,
            "type": "text",
            "text": {"body": message}
        }

        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            logging.info(f"Message sent successfully to {to_number}")
            return True
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error sending WhatsApp message: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" - {e.response.text}"
            logging.error(error_msg)
            return False

    def send_emergency_alert(self, location_info: Dict[str, str]) -> bool:
        """
        Send an emergency alert via WhatsApp.
        
        Args:
            location_info: Dictionary containing 'address' and 'maps_link'
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        trusted_contact = self.config.get('trusted_contact')
        if not trusted_contact:
            logging.error("No trusted contact configured.")
            return False

        try:
            message = (
                f"🚨 *EMERGENCY ALERT* 🚨\n\n"
                f"*{self.config.get('user_name', 'User')}* needs help!\n\n"
                f"📍 *Location:* {location_info.get('address', 'Unknown location')}\n"
                f"🗺️ *Map Link:* {location_info.get('maps_link', 'No location available')}\n\n"
                f"⏰ *Time:* {self._get_current_timestamp()}"
            )
            
            return self.send_message(trusted_contact, message)
        except Exception as e:
            logging.error(f"Error in send_emergency_alert: {e}")
            return False

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in a readable format."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    # Test the WhatsApp sender
    sender = WhatsAppSender()
    test_location = {
        'address': '123 Test St, Test City',
        'maps_link': 'https://www.google.com/maps?q=0,0'
    }
    print("Sending test message...")
    if sender.send_emergency_alert(test_location):
        print("Test message sent successfully!")
    else:
        print("Failed to send test message.")
