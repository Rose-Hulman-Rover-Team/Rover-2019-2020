import asyncore
import socket
import time
import logging
import json


class Client(asyncore.dispatcher_with_send):

    def __init__(self, host, port, message, pk):
        self.logger = logging.getLogger('CLIENT')
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.connect((host, port))
        self.out_buffer = message
        self.clientID = pk
        self.logger.debug('Connected #{}'.format(self.clientID))

    def handle_close(self):
        self.close()

    def handle_read(self):
        rec_msg = self.recv(confjson.get('RATE', None))
        self.logger.debug('#{}, {} back at client {}'.format(self.clientID,
                                                             rec_msg,
                                                             time.time()
                                                             )
                          )
        self.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)s: %(message)s',
                        )

    with open('config.json', 'r') as jfile:
        confjson = json.load(jfile)
    clients = []
    for idx in range(confjson.get('SOCKET_AMOUNT', None)):
        msg = "Start: {}".format(time.time())
        clients.append(Client(confjson.get('HOST', None),
                              confjson.get('PORT', None),
                              msg,
                              idx)
                       )
    start = time.time()
    logging.debug(
        'Starting async loop for all connections, unix time {}'.format(start))
    asyncore.loop()
    i = 0
    while True:
         clients[0].out_buffer = "HELLO"
    logging.debug('{}'.format(time.time() - start))
