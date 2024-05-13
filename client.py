import requests

SERVER_URL = "http://erxt.dev:9000"  # Change this to your server's URL or the server's IP address if not running locally

def play_game(user_id, stake):
    response = requests.post(f"{SERVER_URL}/play", json={"user_id": user_id, "stake": stake})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.json()['message']}")
        return None

def get_statistics(user_id):
    response = requests.get(f"{SERVER_URL}/statistics/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.json()['message']}")
        return None

def check_balance(user_id):
    response = requests.get(f"{SERVER_URL}/balance/{user_id}")
    if response.status_code == 200:
        return response.json()['balance']
    else:
        print(f"Error: {response.json()['message']}")
        return None

def main():
    print("Welcome to the Slot Machine Game!")
    print("1. Login")
    print("2. Create Account")
    choice = input("Choose an option: ")

    if choice == '1':
        user_id = input("Enter your user ID: ")
        user_pw = input("Enter your password: ")
        response = requests.post(f"{SERVER_URL}/login", json={"user_id": user_id, "user_pw": user_pw})
    elif choice == '2':
        user_id = input("Enter your desired user ID: ")
        user_pw = input("Enter your desired password: ")
        response = requests.post(f"{SERVER_URL}/register", json={"user_id": user_id, "user_pw": user_pw})
        if response.status_code != 200:
            print(f"Error: {response.json()['message']}")
            return

    while True:
        print("\n1. Play")
        print("2. Check Balance")
        print("3. View Statistics")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            stake = int(input("Enter your stake: "))
            result = play_game(user_id, stake)
            if result:
                print(result['message'])
                print("Current Slots: " + result['slots'])
                print(f"Your new balance: {result['balance']}")
        elif choice == '2':
            balance = check_balance(user_id)
            print(f"Your current balance is: {balance}")
        elif choice == '3':
            stats = get_statistics(user_id)
            if stats:
                print("Statistics:")
                for key, value in stats.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")
        elif choice == '4':
            print("Exiting the game.")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
