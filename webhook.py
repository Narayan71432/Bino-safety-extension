from flask import Flask, request, jsonify
from whatsapp_sender import WhatsAppSender
from speech_handler import SpeechHandler
from location_service import LocationService
import os
import threading
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Initialize services
whatsapp = WhatsAppSender()
speech_handler = SpeechHandler()
location_service = LocationService()

# Store the last 10 contacts who messaged
recent_contacts = []
MAX_RECENT_CONTACTS = 10

# Store active sessions (phone number -> timestamp)
active_sessions = {}
SESSION_TIMEOUT = 300  # 5 minutes

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verify webhook
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        verify_token = os.getenv('VERIFY_TOKEN', 'bino_emergency')
        
        if mode == 'subscribe' and token == verify_token:
            return challenge, 200
        return 'Verification failed', 403
    
    # Handle incoming messages
    data = request.get_json()
    print(f"Received webhook data: {json.dumps(data, indent=2)}")
    
    try:
        entry = data['entry'][0]
        changes = entry.get('changes', [])
        
        for change in changes:
            if change.get('field') == 'messages':
                value = change.get('value', {})
                messages = value.get('messages', [])
                
                for message in messages:
                    from_number = message.get('from')
                    if not from_number:
                        continue
                        
                    # Add to recent contacts if not already present
                    if from_number not in [c[0] for c in recent_contacts]:
                        recent_contacts.insert(0, (from_number, datetime.now()))
                        # Keep only the most recent contacts
                        if len(recent_contacts) > MAX_RECENT_CONTACTS:
                            recent_contacts.pop()
                    
                    # Check if message contains text
                    if 'text' in message.get('type', '').lower():
                        text = message.get('text', {}).get('body', '').lower()
                        
                        # Check for activation message
                        if 'activate' in text:
                            active_sessions[from_number] = datetime.now()
                            whatsapp.send_message(from_number, "🔊 Bino is now active. Say 'bino' to send emergency alerts to recent contacts.")
                        
                        # Check for wake word
                        elif 'bino' in text and from_number in active_sessions:
                            # Get location and send to recent contacts
                            location = location_service.get_current_location()
                            message = f"🚨 EMERGENCY ALERT from {os.getenv('USER_NAME', 'a user')} 🚨\n\n" \
                                    f"📍 Location: {location.get('address', 'Unknown location')}\n" \
                                    f"🗺️ Map: {location.get('maps_link', 'No location available')}\n\n" \
                                    f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            
                            # Send to recent contacts
                            sent_to = []
                            for contact, _ in recent_contacts:
                                if contact != from_number:  # Don't send to the person who triggered the alert
                                    if whatsapp.send_message(contact, message):
                                        sent_to.append(contact)
                            
                            # Send confirmation
                            if sent_to:
                                whatsapp.send_message(from_number, f"✅ Emergency alert sent to {len(sent_to)} contacts.")
                            else:
                                whatsapp.send_message(from_number, "❌ No contacts available to send the alert to.")
                            
                            # End the session
                            if from_number in active_sessions:
                                del active_sessions[from_number]
    
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
    
    return jsonify({'status': 'ok'}), 200

def cleanup_sessions():
    """Clean up expired sessions."""
    while True:
        now = datetime.now()
        expired = [num for num, ts in active_sessions.items() 
                  if (now - ts).total_seconds() > SESSION_TIMEOUT]
        
        for num in expired:
            del active_sessions[num]
            whatsapp.send_message(num, "⏰ Session expired. Send 'activate' to enable emergency mode again.")
        
        # Sleep for 1 minute
        import time
        time.sleep(60)

if __name__ == '__main__':
    # Start session cleanup thread
    import threading
    thread = threading.Thread(target=cleanup_sessions, daemon=True)
    thread.start()
    
    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
