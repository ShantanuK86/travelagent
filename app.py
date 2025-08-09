#!/usr/bin/env python3
"""
Travel Agent🗺️
A simple AI agent that creates custom vibe boards for travel destinations
Using AutoGen with Gemini free API
"""

import os
import asyncio
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def create_travel_vibe_board(destination: str, api_key: str):
    """
    Creates a travel vibe board for the given destination using direct model client.
    """
    # Configure Gemini model client
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-flash",
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # Create the prompt
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
    from autogen_core.models import SystemMessage, UserMessage
    
    messages = [
        SystemMessage(content=system_prompt),
        UserMessage(content=user_prompt, source="user")
    ]

    try:
        # Get response from the model client
        response = await model_client.create(messages=messages)
        
        if response and response.content:
            print("─" * 80)
            print(response.content)
            print("─" * 80)
        else:
            print("Sorry, I couldn't generate a vibe board for that destination. Please try again!")
    except Exception as e:
        print(f"Error calling model: {str(e)}")
        print("Sorry, I couldn't generate a vibe board for that destination. Please try again!")

def main():
    """Main function to run the Travel Vibe Curator"""
    # Load environment variables
    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("🛑 Please set your GEMINI_API_KEY in the .env file.")
        print("You can get a free API key from Google AI Studio: https://aistudio.google.com/app/apikey")
        return

    print("✨ Welcome to the Travel Vibe Curator! 🗺️")
    print("I'll create custom vibe boards with local phrases, music, food, and first-day plans!")
    print()

    while True:
        destination = input("Enter a travel destination (or 'quit' to exit): ").strip()
        
        if destination.lower() in ['quit', 'exit', 'q']:
            print("Happy travels! 🌟")
            break
        
        if not destination:
            print("Please enter a valid destination!")
            continue
        
        print(f"\n✨ Creating vibe board for {destination}...\n")
        
        try:
            asyncio.run(create_travel_vibe_board(destination, api_key))
        except Exception as e:
            print(f"❌ Error creating vibe board: {str(e)}")
            print("Please try again with a different destination.")
        
        print()

if __name__ == "__main__":
    main()
