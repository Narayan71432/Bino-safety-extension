// Tab switching
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
  button.addEventListener('click', () => {
    // Remove active class from all buttons and contents
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Add active class to clicked button and corresponding content
    button.classList.add('active');
    const tabId = button.getAttribute('data-tab');
    document.getElementById(`${tabId}-tab`).classList.add('active');
  });
});

// Contact Management
const contactNameInput = document.getElementById('contactName');
const contactNumberInput = document.getElementById('contactNumber');
const addContactBtn = document.getElementById('addContact');
const contactsList = document.getElementById('contactsList');
const emergencyBtn = document.getElementById('emergencyBtn');
const statusDiv = document.getElementById('status');

// Load contacts when popup opens
loadContacts();

// Add contact
addContactBtn.addEventListener('click', addContact);

// Handle Enter key in input fields
contactNameInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') contactNumberInput.focus();
});

contactNumberInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') addContact();
});

// Emergency button
emergencyBtn.addEventListener('click', sendEmergencyAlerts);

// Load contacts from storage
function loadContacts() {
  chrome.storage.sync.get(['emergencyContacts'], (result) => {
    const contacts = result.emergencyContacts || [];
    contactsList.innerHTML = '';
    
    if (contacts.length === 0) {
      contactsList.innerHTML = '<p>No contacts added yet.</p>';
      return;
    }
    
    contacts.forEach((contact, index) => {
      const contactElement = document.createElement('div');
      contactElement.className = 'contact-item';
      contactElement.innerHTML = `
        <span>${contact.name} (${contact.number})</span>
        <button class="remove-btn" data-index="${index}">✕</button>
      `;
      contactsList.appendChild(contactElement);
    });
    
    // Add event listeners to remove buttons
    document.querySelectorAll('.remove-btn').forEach(button => {
      button.addEventListener('click', (e) => {
        e.stopPropagation();
        const index = parseInt(button.getAttribute('data-index'));
        removeContact(index);
      });
    });
  });
}

// Add a new contact
function addContact() {
  const name = contactNameInput.value.trim();
  const number = contactNumberInput.value.trim();
  
  if (!name || !number) {
    showStatus('Please enter both name and number', 'error');
    return;
  }
  
  // Basic phone number validation (can be enhanced)
  if (!/^\+?[0-9\s-]{10,}$/.test(number)) {
    showStatus('Please enter a valid phone number', 'error');
    return;
  }
  
  // Get existing contacts
  chrome.storage.sync.get(['emergencyContacts'], (result) => {
    const contacts = result.emergencyContacts || [];
    
    // Check if contact already exists
    if (contacts.some(contact => contact.number === number)) {
      showStatus('This contact already exists', 'error');
      return;
    }
    
    // Add new contact
    contacts.push({ name, number });
    
    // Save to storage
    chrome.storage.sync.set({ emergencyContacts: contacts }, () => {
      // Clear inputs and reload the list
      contactNameInput.value = '';
      contactNumberInput.value = '';
      loadContacts();
      showStatus('Contact added successfully', 'success');
      contactNameInput.focus();
    });
  });
}

// Remove a contact
function removeContact(index) {
  chrome.storage.sync.get(['emergencyContacts'], (result) => {
    const contacts = result.emergencyContacts || [];
    
    if (index >= 0 && index < contacts.length) {
      const contactName = contacts[index].name;
      contacts.splice(index, 1);
      
      // Update storage
      chrome.storage.sync.set({ emergencyContacts: contacts }, () => {
        loadContacts();
        showStatus(`Removed ${contactName}`, 'success');
      });
    }
  });
}

// Send emergency alerts to all contacts
function sendEmergencyAlerts() {
  chrome.storage.sync.get(['emergencyContacts'], (result) => {
    const contacts = result.emergencyContacts || [];
    
    if (contacts.length === 0) {
      showStatus('No contacts to send alerts to', 'error');
      return;
    }
    
    // Get current location
    if (navigator.geolocation) {
      showStatus('Getting your location...', 'success');
      
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          const mapsUrl = `https://www.google.com/maps?q=${latitude},${longitude}`;
          const message = `🚨 EMERGENCY ALERT! 🚨\n\nI need urgent help at this location:\n${mapsUrl}\n\nPlease check on me if possible.`;
          
          // Send message to each contact
          contacts.slice(0, 10).forEach(contact => {
            sendWhatsAppMessage(contact.number, message);
          });
          
          showStatus(`Sent alerts to ${Math.min(contacts.length, 10)} contacts`, 'success');
        },
        (error) => {
          showStatus(`Error getting location: ${error.message}`, 'error');
        },
        { enableHighAccuracy: true, timeout: 10000 }
      );
    } else {
      showStatus('Geolocation is not supported by your browser', 'error');
    }
  });
}

// Send WhatsApp message (opens chat with pre-filled message)
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

// Show status message
function showStatus(message, type = 'success') {
  statusDiv.textContent = message;
  statusDiv.className = type;
  
  // Clear status after 3 seconds
  setTimeout(() => {
    if (statusDiv.textContent === message) {
      statusDiv.textContent = '';
      statusDiv.className = '';
    }
  }, 3000);
}

// Focus on the name field when popup opens
contactNameInput.focus();
