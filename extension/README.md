# Bino Emergency Assistant - Chrome Extension

A Chrome extension that lets you quickly send emergency alerts to your trusted contacts through WhatsApp Web.

## Features

- Add and manage emergency contacts directly in the extension
- One-click emergency alert button
- Automatically includes your current location in alerts
- No server required - works entirely in your browser
- Secure - your contacts are stored locally in Chrome's sync storage

## Installation

1. **Load the extension in Chrome/Edge:**
   - Open Chrome/Edge and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in the top-right corner)
   - Click "Load unpacked" and select the `extension` folder

2. **Pin the extension for easy access:**
   - Click the puzzle piece icon in the top-right corner
   - Find "Bino Emergency" and click the pin icon

## How to Use

1. **Add Emergency Contacts:**
   - Click the Bino Emergency icon in your toolbar
   - Go to the "Contacts" tab
   - Enter a name and phone number (with country code, e.g., +1234567890)
   - Click "Add"
   - Repeat for all your emergency contacts

2. **Send an Emergency Alert:**
   - Click the Bino Emergency icon
   - Go to the "Emergency" tab
   - Click "SEND EMERGENCY ALERT"
   - Allow location access when prompted
   - The extension will open WhatsApp Web with pre-filled messages to all your contacts
   - You'll need to manually click send on each message (due to WhatsApp restrictions)

## How It Works

1. The extension stores your emergency contacts in Chrome's sync storage
2. When you click the emergency button, it gets your current location
3. It opens WhatsApp Web with pre-filled messages containing your location
4. You need to manually send each message (this is a limitation of WhatsApp Web)

## Security & Privacy

- All data is stored locally in your browser
- Your location is only shared when you explicitly click the emergency button
- The extension only requests permissions it needs (storage, geolocation)

## Troubleshooting

- **Location not working:** Make sure you've allowed location access for the extension
- **WhatsApp Web not opening:** Make sure you're logged into WhatsApp Web in your browser
- **Messages not sending:** Due to WhatsApp's restrictions, you'll need to manually click send on each message

## Limitations

- Requires manual sending of messages (WhatsApp Web restriction)
- You must have previously messaged the contacts from your WhatsApp account
- Requires an internet connection to get your location and open WhatsApp Web
