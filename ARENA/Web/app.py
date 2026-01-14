from flask import Flask, render_template, request, redirect, url_for
from models import Player, LeagueOwner, Tournament

app = Flask(__name__)

# --- Mock Database (In-Memory Storage) ---
# We use lists to store data temporarily for Sprint 2
tournaments_db = [
    Tournament(1, "Winter Championship", "Tic-Tac-Toe", "2026-02-01", 64),
    Tournament(2, "Grand Slam", "Chess", "2026-03-15", 32)
]
players_db = []

# --- Routes (Control Logic) ---

@app.route('/')
def home():
    """Display the Home Page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Use Case: Register (Section 2.2.1 [cite: 507])"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        nickname = request.form['nickname']
        
        # Create Player Entity
        new_player = Player(name, email, nickname)
        players_db.append(new_player)
        
        return redirect(url_for('tournaments'))
    
    return render_template('register.html')

@app.route('/tournaments')
def tournaments():
    """Use Case: Browse Tournaments (Section 2.2.1)"""
    return render_template('tournaments.html', tournaments=tournaments_db, players=players_db)

@app.route('/join/<int:tournament_id>', methods=['POST'])
def join_tournament(tournament_id):
    """Use Case: ApplyForTournament (Section 2.3.1 )"""
    # For Sprint 2 demo, we assume the current user is the last registered player
    if not players_db:
        return "Please Register First!"
    
    current_player = players_db[-1] 
    
    for t in tournaments_db:
        if t.id == tournament_id:
            if t.add_player(current_player):
                print(f"Success: {current_player.name} joined {t.name}")
            else:
                print("Error: Tournament Full")
            break
            
    return redirect(url_for('tournaments'))

if __name__ == '__main__':
    app.run(debug=True)