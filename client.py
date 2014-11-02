import common
from message import *

import sys
import urllib2
import logging
import socket
import argparse
import time

class Client:
  def __init__(self, options):
    self.server_ip = options['server_ip']
    self.server_port = options['server_port']
    self.port = options['port']
    self.ip = common.get_public_ip()

    logging.debug("Client settings: {0}".format(vars(self)))

    self.seed = None

  def get_seed(self):
    sock = socket.socket()

  def start(self):
    while True:
      self.seed = self.get_seed()
      time.sleep(5)

  def listen(self):
    pass

  def __create_message(self, message_type, message):
    return Message({'message_type': message_type,
                    'sender_ip': self.ip,
                    'sender_port': self.port,
                    'receiver_ip': self.server_ip,
                    'receiver_port': self.server_port,
                    'message': message})

  def get_seed(self):
    message = self.__create_message(MessageTypes.GET_SEED, '')
    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect((self.server_ip, self.server_port))
      common.send_message(sock, message.serialize())
      received_message = common.recv_message(sock)
      logging.debug('received_message = {0}'.format(received_message))
    except:
      logging.error(sys.exc_info())
    finally:
      sock.close()

def __parse_options():
  parser = argparse.ArgumentParser(description='Process client options.')
  parser.add_argument('-s', "--server", dest="server", type=str,
                      help="Server address, ip & port, port is optional")
  parser.add_argument("-p", "--port", dest="port", type=int,
                      help="Client port")

  args = parser.parse_args()
  print args
  return __filter_options(args)


def __filter_options(args):
  options = {}
  if args.server is not None:
    server_addr = args.server.split(':')
    options['server_ip'] = server_addr[0]

    if len(server_addr) == 1:
      logging.debug('Defaulting to server port {0} !'.format(common.DEFAULT_SERVER_PORT))
      options['server_port'] = common.DEFAULT_SERVER_PORT
    else:
      options['server_port'] = server_addr[1]

  else:
    logging.debug('Defaulting to server {0}:{1} !'.format(common.LOCALHOST_IP, common.DEFAULT_SERVER_PORT))
    options['server_ip'] = common.LOCALHOST_IP
    options['server_port'] = common.DEFAULT_SERVER_PORT

  if args.port is None:
    options['port'] = common.DEFAULT_CLIENT_PORT

  return options

def __main():
  options = __parse_options()
  client = Client(options)
  client.start()

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  __main()