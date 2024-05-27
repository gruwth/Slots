from tk import GUI
from client import Client



if __name__ == "__main__":
    client = Client()
    interface = GUI(client.login, client.register)
    interface.run()







