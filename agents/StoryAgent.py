from swarm import Agent
import openai
import os
import json

# API setup
API_KEY = os.environ.get("Hackathon_API")
client = openai.OpenAI(api_key=API_KEY)


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
    """
    Generates the next part of the story based on context and previous choices.
    Returns a structured story segment with narrative text and choices.

    Args:
        context: Can be either a dictionary with game state or None for initial story
    """
    # Initial story for new game or when context is not a dict
    if context is None or not isinstance(context, dict):
        return {
            "text": """Du vaknar upp i en mörk grotta. Det enda ljuset kommer från en fackla 
            som brinner svagt på väggen. Du hör droppande vatten i fjärran. En kall vind 
            sveper genom grottan och får facklan att fladdra oroväckande.""",
            "choices": [
                "Ta facklan och utforska grottan djupare",
                "Leta efter en väg ut",
                "Ropa efter hjälp",
            ],
        }

    try:
        # If we have valid context, generate next story segment
        previous_choice = str(context.get("previous_choice", "None"))
        player_hp = int(context.get("player_hp", 100))
        location = str(context.get("location", "Unknown"))

        # Create prompt for story generation
        prompt = f"""
        Current game state:
        - Previous action: {previous_choice}
        - Location: {location}
        - Player HP: {player_hp}

        Generate the next story segment in this format:
        {{
            "text": "Detailed situation description",
            "choices": ["Choice 1", "Choice 2", "Choice 3"]
        }}
        """

        try:
            # Generate story using OpenAI API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a fantasy game storyteller.
                     Create engaging narratives and meaningful choices. Format responses as JSON
                     with 'text' and 'choices' keys. Keep descriptions vivid but concise.""",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            # Parse the response
            story_content = response.choices[0].message.content
            try:
                # Try to parse as JSON
                story_data = json.loads(story_content)
            except json.JSONDecodeError:
                # Fallback to default if parsing fails
                story_data = {
                    "text": "Something went wrong with the story generation...",
                    "choices": ["Continue", "Start over"],
                }

            return story_data

        except Exception as e:
            print(f"Error generating story: {e}")
            return {
                "text": "There was an error generating the story...",
                "choices": ["Try again", "Start over"],
            }

    except Exception as e:
        print(f"Error processing context: {e}")
        return {
            "text": "Error processing game state...",
            "choices": ["Start over", "Try again"],
        }


# Story Agent Definition
StoryAgent = Agent(
    name="Story Agent",
    instructions="""You are a storytelling agent for a fantasy adventure game. Your role is to:

    1. Generate engaging narrative content based on player choices
    2. Provide 2-3 meaningful choices that impact the story
    3. Maintain story continuity and reference previous choices
    4. Create atmospheric descriptions that immerse the player
    5. Occasionally introduce combat encounters or challenges
    6. Keep track of player location and status
    
    Story Guidelines:
    - Write in Swedish
    - Keep descriptions vivid but concise (2-3 paragraphs max)
    - Create meaningful choices that impact the story
    - Include a mix of exploration, dialogue, and action
    - Reference previous choices and their consequences
    - Maintain consistent story logic
    - Gradually increase stakes and complexity
    
    When responding:
    1. Always format output as a dictionary with 'text' and 'choices' keys
    2. Ensure 'choices' contains 2-3 distinct options
    3. Keep narrative engaging but focused
    4. Consider the player's current status and location""",
    functions=[generate_story, transfer_to_render, enter_combat],
)
