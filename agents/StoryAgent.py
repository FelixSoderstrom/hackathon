from swarm import Agent
import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

client = openai.OpenAI(api_key=api_key)


def transfer_to_render(context_variables, narrative, choices):
    """
    Transfers control to the render agent with the current narrative and choices.
    """
    from render_agent import (
        render_agent,
    )  # Import at function level to avoid circular imports

    return render_agent


def enter_combat(context_variables, enemy_type):
    """
    Initiates combat sequence when an enemy is encountered.
    """
    from combat_agent import (
        combat_agent,
    )  # Import at function level to avoid circular imports

    return combat_agent


def generate_story(context=None):
    if context is None or not isinstance(context, dict):
        return {
            "text": """Du vaknar upp i en mörk grotta. Det enda ljuset kommer från en fackla 
            som brinner svagt på väggen. Du hör droppande vatten i fjärran. En kall vind 
            sveper genom grottan och får facklan att fladdra oroväckande.
            
            Vad vill du göra?"""
        }

    try:
        user_input = str(context.get("user_input", "None"))
        player_hp = int(context.get("player_hp", 100))
        location = str(context.get("location", "Unknown"))

        prompt = f"""
        Current game state:
        - Player's action: {user_input}
        - Location: {location}
        - Player HP: {player_hp}

        Generate the next story segment in this format:
        {{
            "text": "Detailed situation description followed by 'Vad vill du göra?'"
        }}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a fantasy game storyteller.
                     Create engaging narratives based on the player's free-form input. 
                     Format responses as JSON with 'text' key. 
                     Keep descriptions vivid but concise. Write in Swedish.""",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            story_content = response.choices[0].message.content
            try:
                return json.loads(story_content)
            except json.JSONDecodeError:
                return {
                    "text": "Something went wrong with the story generation...\nVad vill du göra?"
                }

        except Exception as e:
            print(f"Error generating story: {e}")
            return {
                "text": "There was an error generating the story...\nVad vill du göra?"
            }

    except Exception as e:
        print(f"Error processing context: {e}")
        return {"text": "Error processing game state...\nVad vill du göra?"}


# Story Agent Definition
StoryAgent = Agent(
    name="Story Agent",
    instructions="""You are a storytelling agent for a fantasy adventure game. Your role is to:

    1. Generate engaging narrative content based on player's free-form input
    2. Create atmospheric descriptions that immerse the player
    3. Maintain story continuity and reference previous actions
    4. Occasionally introduce combat encounters or challenges
    5. Keep track of player location and status
    
    Story Guidelines:
    - Write in Swedish
    - Keep descriptions vivid but concise (2-3 paragraphs max)
    - Include a mix of exploration, dialogue, and action
    - Reference previous actions and their consequences
    - Maintain consistent story logic
    - Gradually increase stakes and complexity
    
    When responding:
    1. Always format output as a dictionary with 'text' key
    2. End each response with 'Vad vill du göra?'
    3. Keep narrative engaging but focused
    4. Consider the player's current status and location""",
    functions=[generate_story, transfer_to_render, enter_combat],
)
