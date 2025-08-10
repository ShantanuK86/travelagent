#!/usr/bin/env python3
"""
Travel Vibe Curator 🗺️ - Flask Web App with AutoGen
A Flask web application that creates custom vibe boards for travel destinations
Using AutoGen with Gemini API
"""

import os
import asyncio
import json
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv

# Import AutoGen modules with error handling
try:
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_core.models import SystemMessage, UserMessage
    AUTOGEN_AVAILABLE = True
except ImportError as e:
    print(f"AutoGen import error: {e}")
    AUTOGEN_AVAILABLE = False

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

def server_log(level: str, message: str, extra: str = ""):
    """Print formatted log messages to terminal"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")
    if extra:
        print(f"    └─ {extra}")

async def create_travel_vibe_board_async(destination: str, api_key: str):
    """
    Creates a travel vibe board for the given destination using AutoGen.
    """
    server_log("INFO", f"Starting vibe board generation for destination: {destination}")
    
    try:
        # Configure Gemini model client
        server_log("INFO", "Configuring Gemini model client...")
        model_client = OpenAIChatCompletionClient(
            model="gemini-1.5-flash",
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        server_log("SUCCESS", "Gemini model client configured successfully")

        # Create the prompt (same as app.py)
        system_prompt = f"""You are a Travel Agent. Create a comprehensive travel vibe board for any destination.

Your response should include:

🌍 **DESTINATION VIBE BOARD FOR {destination.upper()}**

📍 **Cultural Essentials:**
Present the essential phrases in a neat table format:
| Phrase | Pronunciation | Meaning |
|--------|---------------|---------|
| [Local phrase] | [phonetic guide] | [English meaning] |

Also include:
- Key cultural etiquette tips
- Local customs travelers should know

🎵 **Sound of the City:**
Present the music recommendations in a table format:
| Artist/Song | Genre | Description |
|-------------|-------|-------------|
| [Artist name] | [Genre] | [Brief description] |

Also include:
- Popular music genres in the area
- Spotify playlist suggestions

🍽️ **Taste Adventure:**
- 5-7 must-try local dishes with brief descriptions
- Best food markets or street food areas
- Local dining customs

📅 **First Day Flow:**
- A realistic first-day plan (morning, afternoon, evening)
- Transportation tips
- Budget considerations
- Key logistics (where to go, how long to spend)

Make it visually appealing with emojis and clear sections. Keep it practical and engaging!"""

        user_prompt = f"Create a complete travel vibe board for {destination}. Make it comprehensive and visually appealing!"
        
        # Create messages
        server_log("INFO", "Creating system and user messages...")
        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=user_prompt, source="user")
        ]
        server_log("SUCCESS", f"Messages created successfully - System prompt length: {len(system_prompt)} chars")

        try:
            # Get response from the model client
            server_log("REQUEST", "Sending request to Gemini API...")
            response = await model_client.create(messages=messages)
            
            if response and response.content:
                content_length = len(response.content)
                server_log("SUCCESS", f"Received response from Gemini API", f"Content length: {content_length} characters")
                server_log("SUCCESS", f"Vibe board generation completed for {destination}")
                return {"success": True, "content": response.content}
            else:
                server_log("WARNING", "Empty response received from Gemini API")
                return {"success": False, "error": "Sorry, I couldn't generate a vibe board for that destination. Please try again!"}
                
        except Exception as api_error:
            server_log("ERROR", f"API call failed: {str(api_error)}")
            return {"success": False, "error": f"Error calling model: {str(api_error)}"}
            
    except Exception as e:
        server_log("ERROR", f"Model client configuration failed: {str(e)}")
        return {"success": False, "error": f"Configuration error: {str(e)}"}

# HTML Template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🗺️ Travel Vibe Curator - Flask Edition</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
            overflow: hidden;
        }
        
        .header { 
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4); 
            color: white; 
            text-align: center; 
            padding: 40px 20px;
        }
        
        .header h1 { 
            font-size: 2.5em; 
            margin-bottom: 10px; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p { 
            font-size: 1.2em; 
            opacity: 0.9;
        }
        
        .form-section { 
            padding: 40px; 
            text-align: center;
        }
        
        .input-group { 
            margin-bottom: 20px;
        }
        
        label { 
            display: block; 
            margin-bottom: 10px; 
            font-weight: bold; 
            color: #333;
        }
        
        input[type="text"] { 
            width: 100%; 
            max-width: 400px; 
            padding: 15px; 
            border: 2px solid #ddd; 
            border-radius: 10px; 
            font-size: 16px; 
            transition: border-color 0.3s ease;
        }
        
        input[type="text"]:focus { 
            border-color: #4ECDC4; 
            outline: none; 
            box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.1);
        }
        
        .btn { 
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4); 
            color: white; 
            border: none; 
            padding: 15px 30px; 
            font-size: 18px; 
            border-radius: 10px; 
            cursor: pointer; 
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .btn:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn:disabled { 
            background: #ccc; 
            cursor: not-allowed; 
            transform: none;
        }
        
        .loading { 
            display: none; 
            margin: 20px 0; 
            padding: 20px; 
            background: #f0f8ff; 
            border-radius: 10px; 
            border-left: 5px solid #4ECDC4;
        }
        
        .result { 
            display: none; 
            margin: 20px 0; 
            padding: 30px; 
            background: #f9f9f9; 
            border-radius: 10px; 
            text-align: left; 
            white-space: pre-wrap; 
            line-height: 1.6;
            border-left: 5px solid #4ECDC4;
        }
        
        .error { 
            background: #ffe6e6; 
            border-left-color: #FF6B6B;
        }
        
        .footer { 
            text-align: center; 
            padding: 20px; 
            background: #f8f9fa; 
            color: #666;
        }

        .tech-info {
            background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            border-left: 5px solid #2196F3;
        }

        .tech-info h3 {
            color: #1976D2;
            margin-bottom: 10px;
        }

        .tech-info p {
            color: #424242;
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗺️ Travel Vibe Curator</h1>
            <p>Flask Edition with AutoGen & Gemini AI</p>
        </div>
        
        <div class="tech-info">
            <h3>🔧 Technology Stack</h3>
            <p><strong>Backend:</strong> Flask (Python Web Framework)</p>
            <p><strong>AI Framework:</strong> Microsoft AutoGen</p>
            <p><strong>AI Model:</strong> Google Gemini 1.5 Flash (Free Tier)</p>
            <p><strong>Features:</strong> Async AI calls, Real-time logging, Error handling</p>
        </div>
        
        <div class="form-section">
            <form id="vibeForm">
                <div class="input-group">
                    <label for="destination">🌍 Enter your dream destination:</label>
                    <input type="text" id="destination" name="destination" 
                           placeholder="e.g., Tokyo, Paris, New York..." required>
                </div>
                <button type="submit" class="btn" id="generateBtn">
                    ✨ Create Vibe Board
                </button>
            </form>
            
            <div class="loading" id="loading">
                <h3>🔄 Generating your travel vibe board...</h3>
                <p>Our AI is crafting personalized recommendations for you!</p>
            </div>
            
            <div class="result" id="result"></div>
        </div>
        
        <div class="footer">
            <p>Powered by Flask 🌶️ + AutoGen 🤖 + Gemini AI ⭐</p>
        </div>
    </div>

    <script>
        document.getElementById('vibeForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const destination = document.getElementById('destination').value.trim();
            if (!destination) {
                alert('Please enter a destination!');
                return;
            }
            
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const generateBtn = document.getElementById('generateBtn');
            
            // Show loading state
            loading.style.display = 'block';
            result.style.display = 'none';
            generateBtn.disabled = true;
            generateBtn.textContent = '⏳ Generating...';
            
            try {
                console.log('Sending request for destination:', destination);
                
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ destination: destination })
                });
                
                console.log('Response status:', response.status);
                const data = await response.json();
                console.log('Response data:', data);
                
                loading.style.display = 'none';
                generateBtn.disabled = false;
                generateBtn.textContent = '✨ Create Vibe Board';
                
                if (data.success) {
                    result.textContent = data.content;
                    result.className = 'result';
                    result.style.display = 'block';
                } else {
                    result.textContent = 'Error: ' + data.error;
                    result.className = 'result error';
                    result.style.display = 'block';
                }
            } catch (error) {
                console.error('Network error:', error);
                loading.style.display = 'none';
                generateBtn.disabled = false;
                generateBtn.textContent = '✨ Create Vibe Board';
                
                result.textContent = 'Network error: ' + error.message;
                result.className = 'result error';
                result.style.display = 'block';
            }
        });
        
        // Allow Enter key to submit form
        document.getElementById('destination').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                document.getElementById('vibeForm').dispatchEvent(new Event('submit'));
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Serve the main page"""
    server_log("REQUEST", "GET / - Serving main page")
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_vibe_board():
    """Handle vibe board generation requests"""
    client_ip = request.remote_addr
    server_log("REQUEST", f"POST /generate from {client_ip}")
    
    try:
        data = request.get_json()
        destination = data.get('destination', '').strip()
        server_log("INFO", f"Extracted destination: '{destination}'")
        
        if not AUTOGEN_AVAILABLE:
            server_log("ERROR", "AutoGen is not available - dependencies missing")
            return jsonify({
                "success": False, 
                "error": "AutoGen is not available. Please install required dependencies."
            })
        
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            server_log("ERROR", "GEMINI_API_KEY not configured")
            return jsonify({
                "success": False, 
                "error": "Please set your GEMINI_API_KEY in the .env file."
            })
        
        if not destination:
            server_log("WARNING", "Empty destination received")
            return jsonify({
                "success": False, 
                "error": "Please enter a valid destination!"
            })
        
        server_log("INFO", f"Starting async vibe board generation for: {destination}")
        
        # Run the async function in a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(create_travel_vibe_board_async(destination, api_key))
        finally:
            loop.close()
        
        if response.get("success"):
            server_log("SUCCESS", "Vibe board generation completed successfully")
        else:
            server_log("ERROR", "Vibe board generation failed", response.get("error", "Unknown error"))
        
        server_log("RESPONSE", f"Sending JSON response - Success: {response.get('success', False)}")
        return jsonify(response)
        
    except Exception as e:
        server_log("ERROR", f"Server error during POST processing: {str(e)}")
        return jsonify({
            "success": False, 
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    server_log("REQUEST", "GET /health - Health check")
    return jsonify({
        "status": "healthy",
        "autogen_available": AUTOGEN_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    })

def run_flask_app():
    """Run the Flask application"""
    server_log("STARTUP", "Travel Vibe Curator Flask App initializing")
    
    if not AUTOGEN_AVAILABLE:
        server_log("ERROR", "AutoGen is not available!")
        server_log("INFO", "Please install: pip install autogen-agentchat autogen-ext[openai]")
        return
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        server_log("ERROR", "GEMINI_API_KEY not configured in .env file")
        return
    
    server_log("SUCCESS", "All dependencies and configuration verified")
    server_log("SUCCESS", "Flask app starting on http://localhost:5000")
    server_log("INFO", "Open your browser and visit the URL above!")
    server_log("INFO", "Press Ctrl+C to stop the server")
    
    # Run Flask app without debug mode to avoid threading issues
    app.run(host='0.0.0.0', port=5000, debug=False)

# For Vercel deployment, we need to expose the app object directly
if __name__ == "__main__":
    run_flask_app()
else:
    # Load environment variables for Vercel
    load_dotenv()
