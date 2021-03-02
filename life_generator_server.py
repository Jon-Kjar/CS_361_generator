# utilized the following for help
# url: https://pythonprogramming.net/buffering-streaming-data-sockets-tutorial-python-3/
import socket
import pickle
import life_generator as lg

SERVER_PORT = 5423


class LifeGenServer:
    def __init__(self, port):
        """
        Initiates everything needed for the socket listening
        :param port: port to communicate with the client
        """
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((socket.gethostname(), self.port))
        self.s.listen(5)
        print("<Server> Listening on {}:{}...".format(socket.gethostname(), self.port))

    def __del__(self):
        print('<Server> Destructor called')
        self.s.close()

    def listening(self):
        """
        Starts the loop for communicating with a client
        :return: None
        """
        while True:
            client_socket, address = self.s.accept()
            print("Connection from " + str(address[0]) + " has been established.")

            data = lg.get_top_random_toy()

            msg = pickle.dumps(data)

            # prepend message length to message
            msg = bytes(f'{len(msg):<{10}}', "utf-8") + msg
            client_socket.send(msg)


def main():
    """
    Initiates the life generator server
    :return: None
    """
    lgs = LifeGenServer(SERVER_PORT)
    lgs.listening()


if __name__ == "__main__":
    main()
