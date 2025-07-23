# Bino Emergency Chrome Extension

A Chrome extension that listens for the "bino" wake word and sends emergency alerts to your trusted contacts.

## Features

- One-click activation/deactivation
- Listens for the wake word "bino"
- Sends your location to up to 10 trusted contacts
- Simple interface to manage contacts
- No server required - works locally in your browser

## Installation

1. **Load the extension in Chrome/Edge:**
   - Open Chrome/Edge and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in the top-right corner)
   - Click "Load unpacked" and select the `chrome_extension` folder

2. **Set up trusted contacts:**
   - Click the extension icon and then the "Options" link
   - Add phone numbers of trusted contacts (with country code, e.g., +1234567890)
   - Save your changes

3. **Using the extension:**
   - Click the extension icon to open the popup
   - Click "Activate" to start listening for the wake word
   - Say "bino" to trigger an emergency alert
   - Your location will be sent to your trusted contacts via WhatsApp Web

## How It Works

1. When activated, the extension listens for the wake word "bino" using your computer's microphone
2. When the wake word is detected, it gets your current location
3. It opens WhatsApp Web with a pre-filled message containing your location
4. You need to manually send the message (due to WhatsApp Web restrictions)

## Permissions

- **Microphone**: To listen for the wake word
- **Location**: To get your current location in emergencies
- **Storage**: To save your trusted contacts
- **Tabs**: To open WhatsApp Web when needed

## Troubleshooting

- Make sure you've allowed microphone access when prompted
- Ensure you have an internet connection for location services
- If location isn't accurate, try moving to a location with better GPS signal
- Make sure WhatsApp Web is working in your browser

## Note

This extension requires manual sending of messages due to WhatsApp Web restrictions. For fully automated alerts, you would need to use the WhatsApp Business API.
