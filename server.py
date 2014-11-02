import logging
import socket
import thread

import common
from message import Message

def bind_socket(hostname, port, backlog):
  sock = socket.socket()
  sock.bind((hostname, port))
  sock.listen(backlog)
  return sock

class Server:
  def __init__(self, **kwargs):
    self.hostname = kwargs['hostname']
    self.ip = kwargs['ip']
    self.port = kwargs['port']
    self.backlog = kwargs['backlog']

    self.socket = None

  def start(self):
    logging.debug('Starting Server...')
    self.socket = bind_socket(self.hostname, self.port, self.backlog)
    self.accept_connections()

  def accept_connections(self):
    logging.debug('Listening on {0}:{1}'.format(self.hostname, self.port))
    logging.debug('Public server ip = {0}, port = {1}'.format(common.get_public_ip(), self.port))
    
    while True:
      conn, address = self.socket.accept()
      received_message = common.recv_message(conn)
      thread.start_new_thread(self.handle_request, (conn, received_message))

  def handle_request(self, conn, received_message):
    print received_message
    message = Message.deserialize(received_message)
    logging.debug('received_message: ', message)
    
if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  server = Server(hostname='localhost', ip=common.LOCALHOST_IP, port=common.DEFAULT_SERVER_PORT, backlog=5)
  server.start()




