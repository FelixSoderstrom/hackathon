from swarm import Agent


def render_scene(context=None):
    # Din render logik här
    pass


def display_and_get_input(text):
    """Display the story text and get user input"""
    print("\n" + text + "\n")
    return input("> ")


# Skapa och exportera agenten
render_agent = Agent(
    name="Render Agent",
    instructions="""You are a rendering agent...""",
    functions=[render_scene],
)
