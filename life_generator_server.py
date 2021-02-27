import socket
import pickle
import life_generator as lg
import sys

class LifeGenServer:
    def __init__(self, port):
        """
        :param port: 5423
        """
        msg = lg.get_top_random_toy()
        print(msg)
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((socket.gethostname(), self.port))
        self.s.listen(5)
        print("<Server> Listening on {}:{}...".format(socket.gethostname(), self.port))

    def __del__(self):
        print('<Server> Destructor called')
        self.s.close()

    def start_listening(self):

        while True:
            # now our endpoint knows about the OTHER endpoint.
            client_socket, address = self.s.accept()
            print("Connection from " + str(address[0]) + " has been established.")

            #  input_item_type	input_item_category	input_number_to_generate
            #  toys	            Dogs	              3
            msg = lg.get_top_random_toy()

            data = pickle.dumps(msg)
            print("DATA\t" + str(data))
            msg = bytes(f'{len(data):<{10}}', "utf-8") + data
            client_socket.send(msg)


def main():
    lgs = LifeGenServer(5423)
    lgs.start_listening()


if __name__ == "__main__":
    main()
