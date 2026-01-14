# models.py
# Implements the Entity Objects from Case Study Section 3.5.1 [cite: 842]

class User:
    """Base class for all users [cite: 877]"""
    def __init__(self, name, email, nickname):
        self.name = name
        self.email = email
        self.nickname = nickname

class LeagueOwner(User):
    """Derived class for League Owners [cite: 878]"""
    def __init__(self, name, email, nickname):
        super().__init__(name, email, nickname)
        self.leagues = [] 

class Player(User):
    """Derived class for Players [cite: 880]"""
    def __init__(self, name, email, nickname):
        super().__init__(name, email, nickname)
        self.matches_played = []
        self.points = 0

class Tournament:
    """Represents a Tournament [cite: 856]"""
    def __init__(self, id, name, game_name, start_date, max_players):
        self.id = id
        self.name = name
        self.game_name = game_name
        self.start_date = start_date
        self.max_players = max_players
        self.players = [] # List of registered players
    
    def add_player(self, player):
        if len(self.players) < self.max_players:
            self.players.append(player)
            return True
        return False