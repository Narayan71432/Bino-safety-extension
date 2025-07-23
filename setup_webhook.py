from pyngrok import ngrok
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_webhook():
    """Set up the webhook with ngrok and configure it with WhatsApp."""
    # Set ngrok auth token if provided
    ngrok_auth_token = os.getenv('NGROK_AUTH_TOKEN')
    if ngrok_auth_token and ngrok_auth_token != 'your_ngrok_auth_token':
        ngrok.set_auth_token(ngrok_auth_token)
    
    # Start ngrok tunnel
    port = int(os.getenv('PORT', 5000))
    public_url = ngrok.connect(port).public_url
    print(f" * ngrok tunnel " + public_url)
    
    # Update WhatsApp webhook URL
    whatsapp_token = os.getenv('WHATSAPP_TOKEN')
    phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    verify_token = os.getenv('VERIFY_TOKEN', 'bino_emergency')
    
    if not whatsapp_token or not phone_number_id:
        print("Error: WHATSAPP_TOKEN and WHATSAPP_PHONE_NUMBER_ID must be set in .env")
        return
    
    webhook_url = f"{public_url}/webhook"
    
    # Set up webhook with WhatsApp
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/webhooks"
    headers = {
        'Authorization': f'Bearer {whatsapp_token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'url': webhook_url,
        'verify_token': verify_token,
        'fields': ['messages']
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print("✅ Webhook set up successfully!")
        print(f"   Webhook URL: {webhook_url}")
        print(f"   Verify Token: {verify_token}")
        print("\nTo test the webhook, send a message to your WhatsApp Business number.")
        print("Send 'activate' to start the emergency mode, then say 'bino' to trigger the alert.")
    except Exception as e:
        print(f"❌ Error setting up webhook: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")

if __name__ == '__main__':
    setup_webhook()
