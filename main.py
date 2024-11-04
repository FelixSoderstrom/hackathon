from agents.StoryAgent import StoryAgent, generate_story
from agents.RenderAgent import display_and_get_choice
from agents.CombatAgent import CombatAgent


def run_game():
    print("\nVälkommen till AI Dungeon Master!")
    print("=" * 50)

    # Initialize game context as a dictionary
    context = {
        "player_hp": 100,
        "location": "Dark Cave",
        "previous_choice": None,
        "inventory": [],
    }

    game_active = True

    while game_active:
        try:
            # Generate story and choices
            current_scene = generate_story(context)

            # Get player's choice
            player_choice = display_and_get_choice(
                current_scene["text"], current_scene["choices"]
            )

            # Update context with player's choice and any relevant state changes
            context.update(
                {
                    "previous_choice": player_choice,
                    # Update location based on the choice if needed
                    # "location": new_location_based_on_choice,
                }
            )

            # Check for game-ending conditions
            if player_choice.lower() == "avsluta":
                game_active = False
            elif "died" in current_scene.get("text", "").lower():
                print("\nGame Over!")
                game_active = False
            elif "won" in current_scene.get("text", "").lower():
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
