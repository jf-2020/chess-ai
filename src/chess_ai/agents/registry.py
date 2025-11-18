"""
Agent Registry
--------------

A single, centralized lookup table for creating agents by name.

This registry:
- maps string identifiers to agent classes,
- provides a safe factory (get_agent) to construct agents,
- allows passing configuration parameters (e.g., depth),
- ensures the rest of the system never needs 'if/else' branching on agent names.

This keeps the CLI, web app, and experiment scripts clean, and makes adding new
agents trivial.
"""

from .random_agent import RandomAgent
# Later:
# from .greedy_agent import GreedyAgent
# from .minimax_agent import MinimaxAgent
# from .mcts_agent import MonteCarloTreeSearchAgent

AGENTS = {
    "random": RandomAgent,
    # "greedy": GreedyAgent,
    # "minimax": MinimaxAgent,
    # "mcts": MonteCarloTreeSearchAgent,
}

def get_agent(name: str, **kwargs):
    """
    Construct an agent by name.

    Parameters
    ----------
    name : str
        The registry key identifying which agent to construct.

    kwargs : dict
        Any configuration parameters for that agent.
        For example:
            get_agent("minimax", depth=3, use_alpha_beta=True)

    Returns
    -------
    agent : Player
        An instance of the requested agent.

    Raises
    ------
    KeyError
        If the given name is not registered.
    """

    if name not in AGENTS:
        raise KeyError(
            f"Unknown agent '{name}'."
            f"Available agents: {list(AGENTS.keys())}"
        )
    
    AgentClass = AGENTS[name]
    return AgentClass(**kwargs)