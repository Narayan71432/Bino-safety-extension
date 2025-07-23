document.addEventListener('DOMContentLoaded', function() {
  const phoneInput = document.getElementById('phoneNumber');
  const addButton = document.getElementById('addContact');
  const contactsList = document.getElementById('contacts');
  
  // Load existing contacts
  loadContacts();
  
  // Add contact
  addButton.addEventListener('click', addContact);
  phoneInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      addContact();
    }
  });
  
  // Function to add a new contact
  function addContact() {
    const phoneNumber = phoneInput.value.trim();
    
    // Basic validation
    if (!phoneNumber) {
      alert('Please enter a phone number');
      return;
    }
    
    // Get existing contacts
    chrome.storage.sync.get(['trustedContacts'], function(result) {
      const contacts = result.trustedContacts || [];
      
      // Check if contact already exists
      if (contacts.includes(phoneNumber)) {
        alert('This contact is already in your list');
        return;
      }
      
      // Add new contact
      contacts.push(phoneNumber);
      
      // Save to storage
      chrome.storage.sync.set({ trustedContacts: contacts }, function() {
        // Clear input and reload the list
        phoneInput.value = '';
        loadContacts();
      });
    });
  }
  
  // Function to load and display contacts
  function loadContacts() {
    chrome.storage.sync.get(['trustedContacts'], function(result) {
      const contacts = result.trustedContacts || [];
      contactsList.innerHTML = '';
      
      if (contacts.length === 0) {
        contactsList.innerHTML = '<p>No contacts added yet.</p>';
        return;
      }
      
      // Display each contact with a remove button
      contacts.forEach((contact, index) => {
        const contactElement = document.createElement('div');
        contactElement.className = 'contact-item';
        contactElement.innerHTML = `
          <span>${contact}</span>
          <button class="remove-btn" data-index="${index}">Remove</button>
        `;
        contactsList.appendChild(contactElement);
      });
      
      // Add event listeners to remove buttons
      document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', function() {
          const index = parseInt(this.getAttribute('data-index'));
          removeContact(index);
        });
      });
    });
  }
  
  // Function to remove a contact
  function removeContact(index) {
    chrome.storage.sync.get(['trustedContacts'], function(result) {
      const contacts = result.trustedContacts || [];
      
      if (index >= 0 && index < contacts.length) {
        contacts.splice(index, 1);
        
        // Update storage
        chrome.storage.sync.set({ trustedContacts: contacts }, function() {
          loadContacts();
        });
      }
    });
  }
});
