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


def display_and_get_input(story: str) -> str:
    """
    Display the story and get free-form input from the user.

    Args:
        story: The story text to display

    Returns:
        The player's input
    """
    print("\n" + "=" * 50 + "\n")
    print_with_effect(story)
    print("\n" + "-" * 25 + "\n")

    return input(">> ")
