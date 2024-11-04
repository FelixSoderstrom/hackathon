from agents.StoryAgent import StoryAgent, generate_story
from agents.RenderAgent import display_and_get_input
from agents.CombatAgent import CombatAgent


def run_game():
    print("\nVälkommen till AI Dungeon Master!")
    print("=" * 50)

    # Initialize game context
    context = {
        "player_hp": 100,
        "location": "Dark Cave",
        "user_input": None,
        "inventory": [],
    }

    game_active = True

    while game_active:
        try:
            # Generate story
            story_response = generate_story(context)

            # Ensure story_response has text
            if not isinstance(story_response, dict) or "text" not in story_response:
                raise ValueError("Invalid story response format")

            # Get player's input
            user_input = display_and_get_input(story_response["text"])

            # Update context with player's input
            context["user_input"] = user_input

            # Check for game-ending conditions
            if user_input.lower() in ["avsluta", "quit", "exit"]:
                game_active = False
            elif "died" in story_response["text"].lower():
                print("\nGame Over!")
                game_active = False
            elif "won" in story_response["text"].lower():
                print("\nCongratulations! You've completed the adventure!")
                game_active = False

        except Exception as e:
            print(f"\nError in game loop: {e}")
            retry = input("\nDo you want to continue? (y/n): ").lower()
            if retry != "y":
                game_active = False

    print("\nTack för att du spelade!")


if __name__ == "__main__":
    run_game()
