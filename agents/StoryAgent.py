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


def generate_story(context=None):
    if context is None or not isinstance(context, dict):
        prompt = """Generera en slumpmässig startscen för ett fantasy-äventyr. Välj SLUMPMÄSSIGT från följande:
        - Olika platser (grotta, skog, slott, by, ruiner, tempel, etc)
        - Olika tidpunkter (gryning, skymning, midnatt, etc)
        - Olika väderförhållanden
        - Olika sinnesintryck (ljud, dofter, synintryck)
        - Olika initiala situationer (på flykt, söker skydd, hittat något mystiskt, etc)
        
        Formatera svaret som JSON med 'text'-nyckeln. Avsluta alltid med 'Vad vill du göra?'
        Gör scenen KORT men MÅLANDE. Max 3-4 meningar."""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Du är en kreativ berättare som skapar levande och 
                        varierande scener. Skriv på svenska. Var koncis men målande.""",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.9,
            )

            response_text = response.choices[0].message.content
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return {"text": response_text + "\n\nVad vill du göra?"}

        except Exception as e:
            return {
                "text": """Du vaknar upp i en mörk grotta. Det enda ljuset kommer från en fackla 
                som brinner svagt på väggen. Du hör droppande vatten i fjärran.
                
                Vad vill du göra?"""
            }
    else:
        try:
            user_input = str(context.get("user_input", "None"))
            player_hp = int(context.get("player_hp", 100))
            location = str(context.get("location", "Unknown"))

            prompt = f"""
            Spelläge:
            - Spelarens handling: {user_input}
            - Plats: {location}
            - HP: {player_hp}

            VIKTIGT:
            1. Analysera noga spelarens handling och låt den DIREKT påverka berättelsen
            2. Om spelaren nämner specifika objekt eller riktningar, inkludera dem
            3. Om spelaren visar särskilt intresse för något, utveckla det
            4. Introducera nya element baserat på spelarens val
            5. Låt spelarens handlingar ha konsekvenser
            6. Behåll kontinuitet med tidigare nämnda element

            Generera nästa del av berättelsen och returnera EXAKT i detta format:
            {{
                "text": "Din berättelse här följt av 'Vad vill du göra?'"
            }}
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Du är en responsiv berättare som formar historien 
                        efter spelarens handlingar. Skriv på svenska. Var koncis men följsam 
                        till spelarens intentioner. VIKTIGT: Svara ALLTID i giltigt JSON-format.""",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            response_text = response.choices[0].message.content
            return json.loads(response_text)

        except Exception as e:
            return {
                "text": "Det uppstod ett fel när berättelsen skulle genereras...\nVad vill du göra?"
            }


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
    functions=[generate_story],
)
