from tk import GUI
from client import Client

import time




if __name__ == "__main__":
    client = Client()


    interface = GUI(client.login, client.register, client.get_sorted_lb, client.play, client.get_balance)
    interface.run()









