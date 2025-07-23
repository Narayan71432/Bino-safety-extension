// This script runs in the context of web.whatsapp.com
// It can be used to automatically send messages if needed

console.log('Bino Emergency Assistant content script loaded');

// Listen for messages from the extension
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'sendMessage') {
    // This function would handle automatically sending messages
    // Note: WhatsApp Web has protections against automation
    // This is just a placeholder for future implementation
    console.log('Would send message:', request.message);
  }
});

// Function to automatically send a message (not currently used due to WhatsApp restrictions)
function sendMessageAutomatically(message) {
  const inputBox = document.querySelector('div[title="Type a message"]');
  if (inputBox) {
    inputBox.textContent = message;
    inputBox.dispatchEvent(new Event('input', { bubbles: true }));
    
    const sendButton = document.querySelector('button[data-testid="compose-btn-send"]');
    if (sendButton) {
      sendButton.click();
      return true;
    }
  }
  return false;
}
