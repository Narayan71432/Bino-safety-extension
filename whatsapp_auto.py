import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

class WhatsAppAutomation:
    def __init__(self):
        load_dotenv()
        self.trusted_contacts = self._load_trusted_contacts()
        self.driver = self._setup_driver()
        
    def _load_trusted_contacts(self):
        """Load trusted contacts from environment variable"""
        contacts = os.getenv('TRUSTED_CONTACTS', '').split(',')
        return [c.strip() for c in contacts if c.strip()]
    
    def _setup_driver(self):
        """Setup Chrome WebDriver with options"""
        chrome_options = Options()
        # Uncomment the line below to run in headless mode (no browser window)
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-notifications')
        
        # Set user data directory to maintain session
        user_data_dir = os.path.join(os.path.expanduser('~'), 'whatsapp_auto')
        chrome_options.add_argument(f'user-data-dir={user_data_dir}')
        
        # Initialize Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        return driver
    
    def login_whatsapp(self):
        """Open WhatsApp Web and wait for manual login"""
        print("Opening WhatsApp Web...")
        self.driver.get('https://web.whatsapp.com/')
        
        # Wait for user to scan QR code
        print("Please scan the QR code with your phone...")
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@title="Search or start new chat"]'))
        )
        print("Successfully logged in to WhatsApp Web!")
    
    def send_emergency_message(self, message):
        """Send emergency message to all trusted contacts"""
        if not self.trusted_contacts:
            print("No trusted contacts found. Please set TRUSTED_CONTACTS in .env")
            return
            
        for contact in self.trusted_contacts[:10]:  # Limit to first 10 contacts
            try:
                self._send_message(contact, message)
                print(f"Message sent to {contact}")
                time.sleep(2)  # Small delay between messages
            except Exception as e:
                print(f"Failed to send message to {contact}: {str(e)}")
    
    def _send_message(self, phone_number, message):
        """Send a message to a specific contact"""
        # Open chat with the contact
        chat_url = f'https://web.whatsapp.com/send?phone={phone_number}'
        self.driver.get(chat_url)
        
        # Wait for chat to load
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@title="Type a message"]'))
            )
        except:
            print(f"Could not open chat with {phone_number}. The contact may not exist or you may not have messaged them before.")
            return
        
        # Type and send message
        input_box = self.driver.find_element(By.XPATH, '//div[@title="Type a message"]')
        input_box.click()
        input_box.send_keys(message)
        
        # Click send button
        send_button = self.driver.find_element(By.XPATH, '//button[@data-testid="compose-btn-send"]')
        send_button.click()
        
        # Wait a moment for the message to be sent
        time.sleep(2)
    
    def close(self):
        """Close the browser"""
        self.driver.quit()

def main():
    # Example usage
    whatsapp = WhatsAppAutomation()
    
    try:
        # Login (only needed once per session)
        whatsapp.login_whatsapp()
        
        # Get current location
        location = "My current location: https://www.google.com/maps?q=0,0"  # Replace with actual location
        
        # Create emergency message
        emergency_message = (
            "🚨 EMERGENCY ALERT! 🚨\n\n"
            "I need urgent help at this location:\n"
            f"{location}\n\n"
            "Please check on me if possible."
        )
        
        # Send emergency messages
        print("Sending emergency messages...")
        whatsapp.send_emergency_message(emergency_message)
        print("Emergency messages sent successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Uncomment the line below to automatically close the browser
        # whatsapp.close()
        pass

if __name__ == "__main__":
    main()
