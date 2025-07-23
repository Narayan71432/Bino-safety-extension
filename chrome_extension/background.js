// Initialize default settings
chrome.runtime.onInstalled.addListener(function() {
  // Set default contacts if not already set
  chrome.storage.sync.get(['trustedContacts'], function(result) {
    if (!result.trustedContacts) {
      chrome.storage.sync.set({
        trustedContacts: []
      });
    }
  });
  
  // Set initial active state
  chrome.storage.local.set({ isActive: false });
});

// Listen for messages from popup
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'sendEmergencyAlert') {
    sendEmergencyAlert();
  }
});

// Function to send emergency alert
function sendEmergencyAlert() {
  // This function can be expanded to send notifications or perform other actions
  console.log('Emergency alert triggered');
}
