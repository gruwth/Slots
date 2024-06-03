import requests

class Client:
    def __init__(self):
        self.base_url = "https://slots.erxt.dev"

    
    def register(self, username, password, confirm_password=None):
        res = requests.post(f"{self.base_url}/register-user", json={"user_id": username, "user_pw": password})
        return res
    
    def login(self, username, password):
        res = requests.post(f"{self.base_url}/login", json={"user_id": username, "user_pw": password})
        return res

    def get_leaderboard(self):
        res = requests.get(f"{self.base_url}/leaderboard")
        return res
    
if __name__ == "__main__":
    client = Client()
    lb = client.get_leaderboard()
    users = lb.json()
    sorted_users = sorted(users, key=lambda user: user['money'], reverse=True)
    top_10_users = sorted_users[:10]
    for user in top_10_users:
        print(user)



