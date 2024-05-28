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


if __name__ == "__main__":
    # testing
    import time
    users = [["", ""], ["test", ""], ["", "test"], ["test", "test"], ["test123", "test123"], ["test", "test123"], ["test123", "test"], ["user1", "password1"], ["user2", "password2"], ["user3", "password3"]]
    client = Client()
    for i in range(len(users)):
        res = client.login(users[i][0], users[i][1])
        print(res.status_code, res.json().get("message"))

