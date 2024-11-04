from swarm import Agent


def handle_combat(context=None):
    # Combat logic här
    pass


# Skapa och exportera agenten
CombatAgent = Agent(
    name="Combat Agent",
    instructions="""You are a combat agent...""",
    functions=[handle_combat],
)
