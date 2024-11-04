from swarm import Agent


def initiate_combat(enemy_type="goblin"):
    """
    Startar en combat-sekvens
    """
    return {
        "enemy": enemy_type,
        "enemy_hp": 20,
        "actions": ["Attack", "Defend", "Flee"],
    }


CombatAgent = Agent(
    name="Combat Agent",
    instructions="""Du är en combat agent som hanterar strider i spelet.
    Du följer DnD-liknande regler för combat.""",
    functions=[initiate_combat],
)
