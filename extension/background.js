// Initialize with default values if not set
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.get(['emergencyContacts'], (result) => {
    if (!result.emergencyContacts) {
      chrome.storage.sync.set({ emergencyContacts: [] });
    }
  });
});

// Listen for messages from content scripts or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'sendEmergencyAlert') {
    // Handle emergency alert request
    sendEmergencyAlerts();
  }
});

// Function to send emergency alerts (can be called from background or popup)
function sendEmergencyAlerts() {
  chrome.storage.sync.get(['emergencyContacts'], (result) => {
    const contacts = result.emergencyContacts || [];
    
    if (contacts.length === 0) {
      console.log('No emergency contacts found');
      return;
    }
    
    // Get current location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          const mapsUrl = `https://www.google.com/maps?q=${latitude},${longitude}`;
          const message = `🚨 EMERGENCY ALERT! 🚨\n\nI need urgent help at this location:\n${mapsUrl}\n\nPlease check on me if possible.`;
          
          // Send message to each contact (limit to first 10)
          contacts.slice(0, 10).forEach(contact => {
            sendWhatsAppMessage(contact.number, message);
          });
        },
        (error) => {
          console.error('Error getting location:', error);
        },
        { enableHighAccuracy: true, timeout: 10000 }
      );
    } else {
      console.error('Geolocation is not supported by this browser');
    }
  });
}

// Function to send WhatsApp message
function sendWhatsAppMessage(phoneNumber, message) {
  // Format phone number (remove any non-digit characters except +)
  const formattedNumber = phoneNumber.replace(/[^\d+]/g, '');
  const encodedMessage = encodeURIComponent(message);
  const whatsappUrl = `https://web.whatsapp.com/send?phone=${formattedNumber}&text=${encodedMessage}`;
  
  // Open WhatsApp Web in a new tab
  chrome.tabs.create({ url: whatsappUrl });
  
  // Note: User will need to manually send the message
  // For automatic sending, we'd need to interact with the page using a content script
}
