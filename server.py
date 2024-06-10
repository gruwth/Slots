from flask import Flask, request, jsonify, render_template
import random
import json
import portalocker

app = Flask(__name__)

# Loading user data
def load_user_data():
    with portalocker.Lock('users.json', 'r', timeout=5) as file:
        return json.load(file)

# Saving user data
def save_user_data(data):
    with portalocker.Lock('users.json', 'w', timeout=5) as file:
        json.dump(data, file, indent=4)

class Symbol:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name

symbols = [
    Symbol('a', 1),  # Define symbols and their values
    Symbol('b', 2),
    Symbol('c', 3),
    Symbol('d', 4),
    Symbol('e', 5)
]

symbol_weights = [50, 30, 20, 10, 5]  # Define weights for each symbol

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/game')
def game():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play_game():
    user_id = request.json['user_id']
    stake = request.json['stake']
    if stake == 0:
        return jsonify({"message": "Exiting the game."})

    # Load user data
    users = load_user_data()
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"message": "User not found."}), 404

    if stake > user['money']:
        return jsonify({"message": "You do not have enough money."}), 400

    user['times_played'] += 1
    user['highest_stake'] = max(user['highest_stake'], stake)

    user['money'] -= stake
    slots = random.choices(symbols, weights=symbol_weights, k=5)  # Randomly select symbols
    slots_names = [slots.name for slots in slots]
    slots_output = ' '.join(slot.name for slot in slots)

    symbol_values = {slot.name: slot.value for slot in symbols}  # Create a dictionary of symbol values
    win_amount = 0
    message = 'You lost'

    counts = {slot.name: slots.count(slot) for slot in slots}  # Count the occurrences of each symbol
    common_symbol, common_count = max(counts.items(), key=lambda item: item[1])  # Find the most common symbol

    if common_count == 5:
        win_amount = stake * symbol_values[common_symbol] * 10  # Calculate win amount for 5 matching symbols
        user['all_time_5_wins'] += 1
        message = f'Congratulations! You won: {win_amount}'
    elif common_count == 4:
        win_amount = stake * symbol_values[common_symbol] * 1.5  # Calculate win amount for 4 matching symbols
        user['all_time_4_wins'] += 1
        message = f'You matched four symbols! You won: {win_amount}'
    elif common_count == 3:
        win_amount = stake * symbol_values[common_symbol] * 1  # Calculate win amount for 3 matching symbols
        user['all_time_3_wins'] += 1
        message = f'You matched three symbols! You won: {win_amount}'

    user['money'] += win_amount
    user['all_money_won'] += win_amount
    user['highest_win'] = max(user['highest_win'], win_amount)

    save_user_data(users)
    
    return jsonify({
        "message": message,
        "balance": user['money'],
        "slots": slots_names,
        "statistics": {
            "times_played": user['times_played'],
            "highest_stake": user['highest_stake'],
            "highest_win": user['highest_win'],
            "all_time_3_wins": user['all_time_3_wins'],
            "all_time_4_wins": user['all_time_4_wins'],
            "all_time_5_wins": user['all_time_5_wins'],
            "all_money_won": user['all_money_won']
        },
        "win_amount": win_amount,
        "success": True
    })

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register-user', methods=['POST'])
def register_user():
    user_id = request.json['user_id']
    user_pw = request.json['user_pw']
    users = load_user_data()
    if next((u for u in users if u['id'] == user_id), None):
        return jsonify({"message": "User already exists."}), 400

    users.append({"id": user_id, "pw": user_pw, "money": 1000, "times_played": 0, "highest_stake": 0, "highest_win": 0, "all_time_3_wins": 0, "all_time_4_wins": 0, "all_time_5_wins": 0, "all_money_won": 0})
    save_user_data(users)
    return jsonify({"message": "User registered successfully.", "success": True})

@app.route('/login', methods=['POST'])
def login_user():
    user_id = request.json['user_id']
    user_pw = request.json['user_pw']
    users = load_user_data()
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"message": "User not found."}), 404
    if user['pw'] != user_pw:
        return jsonify({"message": "Invalid password."}), 400
    return jsonify({"message": "User logged in successfully.", "success": True})

@app.route('/statistics/<user_id>', methods=['GET'])
def get_statistics(user_id):
    users = load_user_data()
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"message": "User not found."}), 404

    stats = {
        "times_played": user['times_played'],
        "highest_stake": user['highest_stake'],
        "highest_win": user['highest_win'],
        "all_time_3_wins": user['all_time_3_wins'],
        "all_time_4_wins": user['all_time_4_wins'],
        "all_time_5_wins": user['all_time_5_wins'],
        "all_money_won": user['all_money_won']
    }
    return jsonify(stats)

@app.route('/balance/<user_id>', methods=['GET'])
def check_balance(user_id):
    users = load_user_data()
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"message": "User not found."}), 404
    return jsonify({"balance": user['money']})

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    users = load_user_data()
    users = sorted(users, key=lambda u: u['money'], reverse=True)
    leaderboard = [{"id": u['id'], "money": u['money']} for u in users]
    print(leaderboard)
    return jsonify(leaderboard)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
