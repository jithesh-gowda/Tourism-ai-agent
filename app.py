from flask import Flask, render_template, request, jsonify  # type: ignore
from tourism_system import TourismAIAgent
import os
from datetime import datetime

app = Flask(__name__)
agent = TourismAIAgent()

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌍 Tourism AI Agent</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body { 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                background-size: 400% 400%;
                animation: gradientShift 15s ease infinite;
                min-height: 100vh;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .main-container {
                width: 100%;
                max-width: 900px;
                height: 90vh;
                display: flex;
                flex-direction: column;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 24px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                overflow: hidden;
                animation: slideUp 0.5s ease-out;
            }
            
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px 30px;
                text-align: center;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }
            
            .header h1 {
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 8px;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            }
            
            .header p {
                font-size: 14px;
                opacity: 0.9;
                font-weight: 300;
            }
            
            .examples-container {
                padding: 20px 30px;
                background: #f8f9ff;
                border-bottom: 1px solid #e0e0e0;
                overflow-x: auto;
            }
            
            .examples-container h3 {
                font-size: 14px;
                color: #667eea;
                margin-bottom: 12px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .examples {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            
            .example-chip {
                background: white;
                border: 2px solid #e0e0e0;
                padding: 10px 18px;
                border-radius: 20px;
                font-size: 13px;
                cursor: pointer;
                transition: all 0.3s ease;
                color: #333;
                font-weight: 500;
                white-space: nowrap;
            }
            
            .example-chip:hover {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-color: transparent;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            }
            
            .chat-container { 
                flex: 1;
                padding: 25px 30px;
                overflow-y: auto;
                background: #fafbff;
                scroll-behavior: smooth;
            }
            
            .chat-container::-webkit-scrollbar {
                width: 6px;
            }
            
            .chat-container::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 10px;
            }
            
            .chat-container::-webkit-scrollbar-thumb {
                background: #667eea;
                border-radius: 10px;
            }
            
            .message {
                margin-bottom: 20px;
                display: flex;
                align-items: flex-start;
                gap: 12px;
                animation: messageSlide 0.3s ease-out;
            }
            
            @keyframes messageSlide {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .message-avatar {
                width: 36px;
                height: 36px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                flex-shrink: 0;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            
            .user-message .message-avatar {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            .bot-message .message-avatar {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            }
            
            .message-content {
                flex: 1;
                max-width: 75%;
            }
            
            .message-bubble {
                padding: 14px 18px;
                border-radius: 18px;
                line-height: 1.5;
                word-wrap: break-word;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            }
            
            .user-message {
                flex-direction: row-reverse;
            }
            
            .user-message .message-bubble {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-bottom-right-radius: 4px;
            }
            
            .bot-message .message-bubble {
                background: white;
                color: #333;
                border: 1px solid #e0e0e0;
                border-bottom-left-radius: 4px;
            }
            
            .message-time {
                font-size: 11px;
                color: #999;
                margin-top: 4px;
                padding: 0 4px;
            }
            
            .user-message .message-time {
                text-align: right;
            }
            
            .typing-indicator {
                display: flex;
                gap: 6px;
                padding: 14px 18px;
                background: white;
                border-radius: 18px;
                border: 1px solid #e0e0e0;
                width: fit-content;
            }
            
            .typing-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #667eea;
                animation: typing 1.4s infinite;
            }
            
            .typing-dot:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .typing-dot:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes typing {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.7;
                }
                30% {
                    transform: translateY(-10px);
                    opacity: 1;
                }
            }
            
            .input-container {
                padding: 20px 30px;
                background: white;
                border-top: 1px solid #e0e0e0;
            }
            
            .input-group {
                display: flex;
                gap: 12px;
                align-items: center;
            }
            
            input { 
                flex: 1; 
                padding: 14px 20px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 15px;
                font-family: 'Inter', sans-serif;
                transition: all 0.3s ease;
                outline: none;
            }
            
            input:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .send-button {
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 50%;
                cursor: pointer;
                font-size: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
            
            .send-button:hover:not(:disabled) {
                transform: scale(1.1) rotate(5deg);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            
            .send-button:active:not(:disabled) {
                transform: scale(0.95);
            }
            
            .send-button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            
            .empty-state {
                text-align: center;
                padding: 60px 20px;
                color: #999;
            }
            
            .empty-state-icon {
                font-size: 64px;
                margin-bottom: 16px;
                opacity: 0.5;
            }
            
            .empty-state-text {
                font-size: 16px;
                font-weight: 500;
            }
            
            @media (max-width: 768px) {
                .main-container {
                    height: 100vh;
                    border-radius: 0;
                }
                
                .message-content {
                    max-width: 85%;
                }
                
                .header h1 {
                    font-size: 24px;
                }
            }
        </style>
    </head>
    <body>
        <div class="main-container">
            <div class="header">
                <h1>🌍 Tourism AI Agent</h1>
                <p>Your intelligent travel companion for weather & attractions</p>
            </div>
            
            <div class="examples-container">
                <h3>💡 Quick Examples</h3>
                <div class="examples">
                    <div class="example-chip" onclick="sendExample('What\\'s the weather in Paris?')">What's the weather in Paris?</div>
                    <div class="example-chip" onclick="sendExample('Places to visit in Tokyo')">Places to visit in Tokyo</div>
                    <div class="example-chip" onclick="sendExample('Tell me about New York')">Tell me about New York</div>
                    <div class="example-chip" onclick="sendExample('Weather and attractions in London')">Weather & attractions in London</div>
                    <div class="example-chip" onclick="sendExample('What to see in Dubai?')">What to see in Dubai?</div>
                </div>
            </div>
            
            <div id="chat" class="chat-container">
                <div class="empty-state" id="emptyState">
                    <div class="empty-state-icon">✈️</div>
                    <div class="empty-state-text">Start a conversation to explore destinations!</div>
                </div>
            </div>
            
            <div class="input-container">
                <div class="input-group">
                    <input type="text" id="message" placeholder="Ask about any place... (e.g., 'Weather in Paris' or 'Attractions in Tokyo')" onkeypress="handleKeyPress(event)">
                    <button class="send-button" id="sendButton" onclick="sendMessage()" title="Send message">
                        ➤
                    </button>
                </div>
            </div>
        </div>

        <script>
            let isLoading = false;
            
            function getCurrentTime() {
                const now = new Date();
                return now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
            }
            
            function hideEmptyState() {
                const emptyState = document.getElementById('emptyState');
                if (emptyState) {
                    emptyState.style.display = 'none';
                }
            }
            
            function showTypingIndicator() {
                hideEmptyState();
                const chat = document.getElementById('chat');
                const typingDiv = document.createElement('div');
                typingDiv.className = 'message bot-message';
                typingDiv.id = 'typingIndicator';
                typingDiv.innerHTML = `
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">
                        <div class="message-bubble typing-indicator">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                `;
                chat.appendChild(typingDiv);
                scrollToBottom();
            }
            
            function removeTypingIndicator() {
                const typingIndicator = document.getElementById('typingIndicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
            }
            
            function addMessage(message, isUser = false) {
                hideEmptyState();
                removeTypingIndicator();
                
                const chat = document.getElementById('chat');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
                
                const avatar = isUser ? '👤' : '🤖';
                const time = getCurrentTime();
                
                messageDiv.innerHTML = `
                    <div class="message-avatar">${avatar}</div>
                    <div class="message-content">
                        <div class="message-bubble">${formatMessage(message)}</div>
                        <div class="message-time">${time}</div>
                    </div>
                `;
                
                chat.appendChild(messageDiv);
                scrollToBottom();
            }
            
            function formatMessage(message) {
                // Convert line breaks to <br>
                let formatted = message.replace(/\\n/g, '<br>');
                // Format bullet points
                formatted = formatted.replace(/•/g, '•');
                // Add some basic formatting
                return formatted;
            }
            
            function scrollToBottom() {
                const chat = document.getElementById('chat');
                setTimeout(() => {
                    chat.scrollTop = chat.scrollHeight;
                }, 100);
            }
            
            async function sendMessage(messageText = null) {
                if (isLoading) return;
                
                const input = document.getElementById('message');
                const sendButton = document.getElementById('sendButton');
                const message = messageText || input.value.trim();
                
                if (!message) return;
                
                isLoading = true;
                sendButton.disabled = true;
                
                addMessage(message, true);
                if (!messageText) input.value = '';
                
                showTypingIndicator();
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        addMessage('❌ ' + data.error);
                    } else {
                        addMessage(data.response);
                    }
                } catch (error) {
                    addMessage('❌ Error: Unable to connect to server. Please try again.');
                } finally {
                    isLoading = false;
                    sendButton.disabled = false;
                    if (!messageText) input.focus();
                }
            }
            
            function sendExample(exampleText) {
                const input = document.getElementById('message');
                input.value = exampleText;
                sendMessage(exampleText);
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    sendMessage();
                }
            }
            
            // Focus input on load
            window.onload = function() {
                document.getElementById('message').focus();
            }
        </script>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = agent.process_request(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)