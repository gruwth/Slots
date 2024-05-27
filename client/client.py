import requests

from tk import GUI


class Client:
    def __init__(self):
        self.base_url = "https://slots.erxt.dev"

    
    def register(self, username, password, confirm_password):
        res = requests.post(f"{self.base_url}/register-user", json={"user_id": username, "user_pw": password})
    
    def login(self, username, password):
        res = requests.post(f"{self.base_url}/login", json={"user_id": username, "user_pw": password})
        print(res.json())

    
