class Player:
    """
    Base class for anything that can choose a move:
    - human (via CLI or GUI)
    - random agent
    - neural net agent
    - search agent
    """
    def choose_move(self, game):
        raise NotImplementedError