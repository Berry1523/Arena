import datetime

# --- Entity Layer (Data & Core Logic) ---
# Based on Section 6.1: Entity Objects 

class User:
    """Base class for all users [cite: 190]"""
    def __init__(self, name, email, nickname):
        self.name = name
        self.email = email
        self.nickname = nickname

class LeagueOwner(User):
    """Derived class for League Owners [cite: 194]"""
    def __init__(self, name, email, nickname):
        super().__init__(name, email, nickname)
        self.leagues = [] # A list to hold leagues owned by this user

    def add_league(self, league):
        self.leagues.append(league)

class Game:
    """Represents a Game (e.g., TicTacToe) [cite: 185]"""
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

class League:
    """Represents a League associated with a game [cite: 176]"""
    def __init__(self, name, game, owner, max_tournaments=5):
        self.name = name
        self.game = game
        self.owner = owner
        self.max_tournaments = max_tournaments
        self.tournaments = [] # List of tournaments in this league

    def add_tournament(self, tournament):
        self.tournaments.append(tournament)

class Tournament:
    """Represents a specific Tournament event [cite: 179]"""
    def __init__(self, name, start_date, max_players):
        self.name = name
        self.start_date = start_date
        self.max_players = max_players
        self.status = "Announced"

    def __repr__(self):
        return f"<Tournament: {self.name} | Max Players: {self.max_players}>"

# --- Control Layer (Business Logic) ---
# Based on Section 6.5: Control Objects [cite: 217]

class AnnounceTournamentControl:
    """
    Coordinates the tournament announcement workflow.
    Implements the logic from Sequence Diagram 7.1.
    """
    
    def create_tournament(self, league_owner, league, name, start_date, max_players):
        print(f"\n[System] Initiating Tournament Creation for League: {league.name}...")

        # 1. Validation: Check if the requester is actually the owner of the league
        if league not in league_owner.leagues:
            print("[Error] Permission Denied: User does not own this league.")
            return False

        # 2. Validation: Check Max Tournaments (Business Rule) 
        if len(league.tournaments) >= league.max_tournaments:
            print("[Error] Limit Exceeded: League has reached max tournaments.")
            return False

        # 3. Create the Tournament Entity [cite: 235]
        new_tournament = Tournament(name, start_date, max_players)
        
        # 4. Associate Tournament with League [cite: 236]
        league.add_tournament(new_tournament)
        
        print(f"[Success] Tournament '{name}' created successfully!")
        return new_tournament

# --- Main Execution Block (for Demonstration) ---
if __name__ == "__main__":
    print("=== ARENA SYSTEM: SPRINT 1 DEMO ===")
    
    # 1. Setup: Create a Game and a League Owner
    print("\n1. Setting up Environment (Game & Owner)...")
    tic_tac_toe = Game("Tic-Tac-Toe", "Standard 3x3 Rules")
    owner_alice = LeagueOwner("Alice", "alice@arena.com", "AliceTheBoss")
    
    # 2. Owner creates a League
    print("\n2. Alice creates the 'Pro Tic-Tac-Toe League'...")
    pro_league = League("Pro Tic-Tac-Toe League", tic_tac_toe, owner_alice)
    owner_alice.add_league(pro_league)
    print(f"   League '{pro_league.name}' ready.")

    # 3. Use Case: Announce Tournament (Using Control Object)
    # This mirrors the Sequence Diagram in Section 7.1 
    controller = AnnounceTournamentControl()
    
    # Test 1: Successful Creation
    t1 = controller.create_tournament(
        league_owner=owner_alice,
        league=pro_league,
        name="Winter Championship 2026",
        start_date="2026-02-01",
        max_players=64
    )

    # Test 2: Validation Check (Trying to create a tournament for a league Alice doesn't own)
    print("\n4. Testing Security/Validation...")
    fake_league = League("Fake League", tic_tac_toe, None) # No owner
    controller.create_tournament(owner_alice, fake_league, "Hacked Event", "2026-02-01", 10)

    # 5. Final State Check
    print("\n5. Verifying System State...")
    print(f"   Tournaments in {pro_league.name}:")
    for t in pro_league.tournaments:
        print(f"   - {t}")