let isActive = false;
let recognition = null;

// Elements
const toggleBtn = document.getElementById('toggleBtn');
const statusDiv = document.getElementById('status');
const logDiv = document.getElementById('log');

// Load saved state
chrome.storage.local.get(['isActive'], function(result) {
  isActive = result.isActive || false;
  updateUI();
});

// Toggle activation
function toggleActivation() {
  isActive = !isActive;
  chrome.storage.local.set({ isActive: isActive }, function() {
    updateUI();
    if (isActive) {
      startListening();
      log('Emergency mode activated. Listening for "bino"...');
    } else {
      stopListening();
      log('Emergency mode deactivated.');
    }
  });
}

// Update UI based on current state
function updateUI() {
  if (isActive) {
    toggleBtn.textContent = 'Deactivate';
    toggleBtn.classList.add('active');
    statusDiv.textContent = 'Status: Active (Listening for "bino")';
    statusDiv.className = 'active';
  } else {
    toggleBtn.textContent = 'Activate';
    toggleBtn.classList.remove('active');
    statusDiv.textContent = 'Status: Inactive';
    statusDiv.className = 'inactive';
  }
}

// Log messages to the popup
function log(message) {
  const logEntry = document.createElement('div');
  logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  logDiv.prepend(logEntry);
  
  // Keep only the last 5 log entries
  while (logDiv.children.length > 5) {
    logDiv.removeChild(logDiv.lastChild);
  }
}

// Start listening for "bino"
function startListening() {
  try {
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = false;
    
    recognition.onresult = function(event) {
      const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase().trim();
      log(`Heard: "${transcript}"`);
      
      if (transcript.includes('bino')) {
        log('Emergency word detected! Sending alerts...');
        sendEmergencyAlert();
      }
    };
    
    recognition.onerror = function(event) {
      log(`Error occurred in recognition: ${event.error}`);
    };
    
    recognition.start();
    log('Started listening for "bino"...');
    
  } catch (error) {
    log(`Error initializing speech recognition: ${error.message}`);
  }
}

// Stop listening
function stopListening() {
  if (recognition) {
    recognition.stop();
    recognition = null;
  }
}

// Send emergency alert
function sendEmergencyAlert() {
  // Get current location
  if (navigator.geolocation) {
    log('Getting your location...');
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        const mapsLink = `https://www.google.com/maps?q=${latitude},${longitude}`;
        
        // Get trusted contacts from storage
        chrome.storage.sync.get(['trustedContacts'], function(result) {
          const contacts = result.trustedContacts || [];
          
          if (contacts.length === 0) {
            log('No trusted contacts found. Please add contacts in the options page.');
            return;
          }
          
          // Send message to each contact
          contacts.slice(0, 10).forEach(contact => {
            sendWhatsApp(contact, `🚨 EMERGENCY ALERT! 🚨\n\nI need help at this location:\n${mapsLink}`);
          });
          
          log(`Sent emergency alerts to ${Math.min(contacts.length, 10)} contacts.`);
        });
      },
      (error) => {
        log(`Error getting location: ${error.message}`);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
  } else {
    log('Geolocation is not supported by this browser.');
  }
}

// Send WhatsApp message (using web.whatsapp.com)
function sendWhatsApp(phoneNumber, message) {
  const encodedMessage = encodeURIComponent(message);
  const whatsappUrl = `https://web.whatsapp.com/send?phone=${phoneNumber}&text=${encodedMessage}`;
  
  // Open WhatsApp Web in a new tab
  chrome.tabs.create({ url: whatsappUrl });
  
  // Note: This will require the user to manually send the message
  // For automatic sending, you would need the WhatsApp Business API
  log(`Opened WhatsApp chat with ${phoneNumber}. Please send the message.`);
}

// Event listeners
toggleBtn.addEventListener('click', toggleActivation);

// Initialize
updateUI();
if (isActive) {
  startListening();
}
