#!/usr/bin/env python3
"""
Travel Vibe Curator 🗺️ - Streamlit Web App
A simple AI agent that creates custom vibe boards for travel destinations
Using AutoGen with Gemini free API (Web Version of app.py)
"""

import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

# Import AutoGen modules with error handling
try:
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_core.models import SystemMessage, UserMessage
    AUTOGEN_AVAILABLE = True
except ImportError as e:
    st.error(f"AutoGen import error: {e}")
    AUTOGEN_AVAILABLE = False

# Load environment variables
load_dotenv()

async def create_travel_vibe_board_web(destination: str, api_key: str):
    """
    Creates a travel vibe board for the given destination using direct model client.
    This is the web version of the function from app.py
    """
    # Configure Gemini model client
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash",
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

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
    
    # Create messages (same as app.py)
    messages = [
        SystemMessage(content=system_prompt),
        UserMessage(content=user_prompt, source="user")
    ]

    try:
        # Get response from the model client
        response = await model_client.create(messages=messages)
        
        if response and response.content:
            return response.content
        else:
            return "Sorry, I couldn't generate a vibe board for that destination. Please try again!"
    except Exception as e:
        return f"Error calling model: {str(e)}\nSorry, I couldn't generate a vibe board for that destination. Please try again!"

def main():
    """Main Streamlit app"""
    # Page configuration
    st.set_page_config(
        page_title="Travel Vibe Curator",
        page_icon="🗺️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #4ECDC4;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .result-container {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 5px solid #4ECDC4;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<h1 class="main-header">🗺️ Travel Vibe Curator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create custom vibe boards with local phrases, music, food, and first-day plans!</p>', unsafe_allow_html=True)

    # Check for API key and AutoGen availability (same logic as app.py)
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not AUTOGEN_AVAILABLE:
        st.error("❌ AutoGen is not available. Please install the required dependencies.")
        st.code("pip install autogen-agentchat autogen-ext[openai]")
        st.stop()
    
    if not api_key or api_key == "your_gemini_api_key_here":
        st.error("🛑 Please set your GEMINI_API_KEY in the .env file.")
        st.info("You can get a free API key from Google AI Studio: https://aistudio.google.com/app/apikey")
        st.stop()

    # Main input section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        destination = st.text_input(
            "🌍 Enter a travel destination:",
            placeholder="e.g., Tokyo, Paris, Delhi, Bangkok...",
            help="Enter any city or country you'd like to explore!"
        )
        
        generate_button = st.button("✨ Create Vibe Board", use_container_width=True)

    # Generate vibe board when button is clicked
    if generate_button and destination:
        if destination.strip():
            with st.spinner(f"🌟 Creating vibe board for {destination}..."):
                try:
                    # Use the same async function logic as app.py
                    result = asyncio.run(create_travel_vibe_board_web(destination.strip(), api_key))
                    
                    # Display result in a nice container
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add download button
                    st.download_button(
                        label="📄 Download Vibe Board as Text",
                        data=result,
                        file_name=f"{destination.lower().replace(' ', '_')}_vibe_board.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error creating vibe board: {str(e)}")
                    st.error("Please try again with a different destination.")
        else:
            st.warning("⚠️ Please enter a valid destination!")
    
    elif generate_button and not destination:
        st.warning("⚠️ Please enter a destination first!")

    # Sidebar with examples and info
    with st.sidebar:
        st.markdown("### 🌟 Popular Destinations")
        st.markdown("Click any destination below to try it out:")
        
        example_destinations = [
            ("🇯🇵", "Tokyo"), ("🇫🇷", "Paris"), ("🇮🇳", "Delhi"), ("🇹🇭", "Bangkok"),
            ("🇺🇸", "New York"), ("🇬🇧", "London"), ("🇪🇸", "Barcelona"), ("🇮🇹", "Rome"),
            ("🇦🇺", "Sydney"), ("🇧🇷", "Rio de Janeiro"), ("🇪🇬", "Cairo"), ("🇿🇦", "Cape Town")
        ]
        
        for flag, city in example_destinations:
            if st.button(f"{flag} {city}", key=f"example_{city}", use_container_width=True):
                st.session_state.destination_input = city
                st.experimental_rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ About This App")
        st.markdown("""
        This Travel Vibe Curator creates personalized travel guides including:
        
        📍 **Cultural Essentials**  
        Local phrases with pronunciation & cultural etiquette
        
        🎵 **Sound of the City**  
        Music recommendations & playlist suggestions
        
        🍽️ **Taste Adventure**  
        Must-try foods & dining customs
        
        📅 **First Day Flow**  
        Complete itinerary with transportation tips
        
        **Powered by:** AutoGen + Gemini AI  
        **Console Version:** Run `python app.py`
        """)
        
        st.markdown("---")
        st.markdown("### 🛠️ Technical Details")
        st.markdown("""
        - **Framework**: Streamlit + AutoGen
        - **AI Model**: Google Gemini 1.5 Flash
        - **Features**: Table formatting, downloadable guides
        - **API**: Free Gemini API from Google AI Studio
        """)

    # Handle example destination selection
    if 'destination_input' in st.session_state:
        st.session_state.destination_input = st.session_state.destination_input

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888; margin-top: 2rem;'>"
        "Made with ❤️ using AutoGen, Gemini AI & Streamlit | Happy Travels! 🌟<br>"
        "<small>This is the web version of the console app in app.py</small>"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
