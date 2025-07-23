# Bino Emergency Assistant

A voice-activated emergency alert system that sends your location to a trusted contact via WhatsApp when you say the wake word "Bino" followed by an emergency phrase.

## Features

- 🔔 Wake word detection ("Bino")
- 🚨 Emergency phrase recognition
- 📍 Automatic location detection
- 💬 WhatsApp Business API integration
- 🔒 Secure configuration with environment variables
- 🎤 Voice feedback
- 🎨 Colorful console output

## Requirements

- Python 3.7+
- Microphone
- Internet connection
- WhatsApp Business API access

## Setup Instructions

1. **Get WhatsApp Business API Credentials**
   - Go to [Meta for Developers](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
   - Create a new app and get your API token and phone number ID
   - Save these credentials in your `.env` file (see `.env.example`)

2. **Set Up Webhook**
   - Install ngrok (https://ngrok.com/download)
   - Get your ngrok auth token from https://dashboard.ngrok.com/get-started/your-authtoken
   - Add it to your `.env` file as `NGROK_AUTH_TOKEN`
   - Run `python setup_webhook.py` to set up the webhook
   - This will give you a public URL that you need to configure in your WhatsApp App Settings

3. **Configure Webhook in Meta Developer Dashboard**
   - Go to your WhatsApp App in Meta Developer Dashboard
   - Under "Configure Webhooks", enter the webhook URL from the setup script
   - Set the Verify Token to match the one in your `.env` file (default: 'bino_emergency')

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/bino-emergency-assistant.git
   cd bino-emergency-assistant
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application:
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your WhatsApp API credentials and trusted contact
   ```env
   # WhatsApp API Configuration
   WHATSAPP_TOKEN=your_api_token_here
   WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
   
   # Emergency Contact
   TRUSTED_CONTACT=+1234567890
   
   # User Information
   USER_NAME="Your Name"
   EMERGENCY_MESSAGE="🚨 I need help!"
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Say "Bino" to wake up the assistant
3. When prompted, say an emergency phrase like "I'm in danger" or "Help me"
4. The assistant will get your location and send it to your trusted contact

## How It Works

1. The assistant continuously listens for the wake word "Bino"
2. After hearing the wake word, it listens for emergency phrases
3. When an emergency is detected, it fetches your current location using IP geolocation
4. It sends a WhatsApp message to your trusted contact with your location and a Google Maps link
5. The assistant provides voice feedback throughout the process

## Security Considerations

- 🔒 Never commit your `.env` file to version control
- 🔑 Keep your WhatsApp API token secure
- 👥 Only share your trusted contact number with people you trust
- 🌐 Consider using a VPN if privacy is a concern

## Troubleshooting

### Common Issues

#### Microphone Access
- **Issue**: "No microphone found" or similar error
- **Solution**:
  - Ensure your microphone is properly connected
  - Check system permissions for microphone access
  - Try listing available devices with `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

#### WhatsApp API
- **Issue**: Messages not being delivered
- **Solution**:
  - Verify your WhatsApp API token and phone number ID
  - Check your Meta Developer Dashboard for any restrictions
  - Ensure the recipient's number is in the correct format with country code

#### Location Inaccuracies
- **Issue**: Location is not accurate
- **Solution**:
  - The app uses IP-based geolocation which may not be precise
  - For better accuracy, consider enabling GPS on your device

## Future Enhancements

### Priority
- [ ] Add GPS location support for better accuracy
- [ ] Implement message templates for different emergency types
- [ ] Add message delivery status callbacks

### Planned
- [ ] Create a web dashboard for configuration
- [ ] Add support for multiple trusted contacts
- [ ] Implement end-to-end encryption for messages
- [ ] Create a mobile app with background service

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ❤️ using Python
- Uses the [whatsapp-chatbot-python](https://github.com/green-api/whatsapp-chatbot-python) library
- Inspired by the need for personal safety solutions

## 🙏 Acknowledgments

- Inspired by the WhatsApp-based search assistant Bino
- Built with Python and open-source libraries
- Special thanks to all contributors and open-source maintainers

---

💡 **Note**: This is a personal safety tool. Always have multiple safety measures in place and don't rely solely on this application in emergency situations.
