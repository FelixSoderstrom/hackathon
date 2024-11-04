from swarm import Agent
from typing import List, Dict
import time


def print_with_effect(text: str, delay: float = 0.01):
    """
    Print text with a typewriter effect

    Args:
        text: The text to print
        delay: Delay between each character
    """
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def display_and_get_choice(story: str, choices: List[str]) -> str:
    """
    Display the story and choices, then get user input.

    Args:
        story: The story text to display
        choices: List of choices for the player

    Returns:
        The player's selected choice
    """
    # Clear some space and print story
    print("\n" + "=" * 50 + "\n")
    print_with_effect(story)
    print("\n" + "-" * 25 + " Choices " + "-" * 25 + "\n")

    # Display numbered choices
    for idx, choice in enumerate(choices, 1):
        print_with_effect(f"{idx}. {choice}")

    # Get and validate input
    while True:
        try:
            choice = int(input("\nEnter your choice (number): "))
            if 1 <= choice <= len(choices):
                return choices[choice - 1]
            print("Please enter a valid number.")
        except ValueError:
            print("Please enter a number.")


# Create the RenderAgent instance
render_agent = Agent(
    name="RenderAgent",
    instructions="""You are a rendering agent that displays story content to the player.
    Your primary function is to take story content and choices from the StoryAgent,
    display them appropriately, and return the player's choice.""",
    functions=[display_and_get_choice],
)
