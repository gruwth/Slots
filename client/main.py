from tk import GUI
from client import Client

import time




if __name__ == "__main__":
    client = Client()

    def get_init_lb():
        lb = client.get_leaderboard().json()
        sorted_users = sorted(lb, key=lambda user: user['money'], reverse=True)
        return(sorted_users[:10])

    interface = GUI(client.login, client.register, get_init_lb, client.play)
    interface.run()







