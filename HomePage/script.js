// Initialize Lucide Icons
// Whenever lucide.createIcons() is called, the i tags with data-lucide attributes are replaced with
// svg tags that create the icons.
lucide.createIcons();

// Chatbot Logic
const chatbotToggle = document.getElementById('chatbot-toggle'); 
const chatbotWindow = document.getElementById('chatbot-window'); 
const chatInput = document.getElementById('chat-input'); 
const chatSend = document.getElementById('chat-send'); 
const chatMessages = document.getElementById('chat-messages'); 
const toggleIcon = chatbotToggle.querySelector('i');

let isOpen = false;

// Toggle Chatbot Window 
chatbotToggle.addEventListener('click', () => { 
    isOpen = !isOpen; 
    if (isOpen) { 
        chatbotWindow.classList.remove('d-none'); 
        chatbotWindow.classList.add('d-flex');
        chatbotToggle.innerHTML = `<i data-lucide="x" width="24" height="24"></i>`;                 // Change icon to X
    } 
    else { 
        chatbotWindow.classList.remove('d-flex'); 
        chatbotWindow.classList.add('d-none'); 
        chatbotToggle.innerHTML = `<i data-lucide="message-circle" width="24" height="24"></i>`;    // Change icon to message-circle
    }
    lucide.createIcons(); // Refresh icons 
});

// Send Message Logic 
function handleSend() { 
    const text = chatInput.value.trim(); 
    if (!text) return;
    // Add User Message
    appendMessage(text, 'user');
    chatInput.value = '';

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Simulate AI Response
    setTimeout(() => {
        const responses = [
            "For wheat cultivation, ensure soil pH is between 6.0-7.5 and sow during October-November.",
            "To control aphids, use neem oil spray (5ml/liter) or introduce ladybugs as biological control.",
            "Current wheat market price in Punjab is ₹2,100/quintal (as of Jan 2026).",
            "Yellow leaves often indicate nitrogen deficiency. Apply urea @ 20-25 kg/acre."
        ];
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
        appendMessage(randomResponse, 'bot');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
}

// Append Message to UI 
function appendMessage(text, type) { 
    const msgDiv = document.createElement('div'); 
    msgDiv.className = `d-flex mb-3 ${type === 'user' ? 'justify-content-end' : 'justify-content-start'}`;
    const bubble = document.createElement('div');
    bubble.className = `p-3 rounded-4 ${type === 'user' ? 'bg-success text-white rounded-bottom-right-0' : 'bg-white border text-dark rounded-bottom-left-0'}`;
    bubble.style.maxWidth = '85%';

    const p = document.createElement('p');
    p.className = 'mb-0 small';
    p.textContent = text;

    bubble.appendChild(p);
    msgDiv.appendChild(bubble);
    chatMessages.appendChild(msgDiv);
}

// Event Listeners for Sending 
chatSend.addEventListener('click', handleSend); 
chatInput.addEventListener('keypress', (e) => { 
    if (e.key === 'Enter') handleSend(); 
});