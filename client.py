from common import *

import sys
import urllib2
import logging
import socket
from optparse import OptionParser

class Client:
  def __init__(self, options):
    self.server_ip = options['server_ip']
    self.server_port = options['server_port']
    self.port = options['port']
    self.ip = get_ip()

    logging.debug("Client settings: {0}".format(vars(self)))

    self.seed = None

  def get_seed(self):
    sock = socket.socket()

  def start(self):
    while True:
      self.seed = get_seed()



  def listen(self):
    pass



def get_ip():
  try:
    ip = urllib2.urlopen(GET_PUBLIC_IP_URL).read()
  except:
    logging.debug('Failed to query external server to get my public ip ! Defaulting to 127.0.0.1')
    ip = '127.0.0.1'
  return ip

def parse_options(params):
  parser = OptionParser()
  parser.add_option("-s", "--server", dest="server", type="string",
                    help="Server address, ip & port, port is optional")
  parser.add_option("-p", "--port", dest="port", type="int",
                    help="Client port")
  (options, args) = parser.parse_args()

  options = vars(options)

  if len(args) > 0:
    logging.error('Some command line arguments could not be processed: {0}!'.format(args))
    logging.error('Exiting...')
    sys.exit()

  return filter_options(options)

def filter_options(options):
  if options['server'] is not None:
    server_addr = options['server'].split(':')
    del options['server']
    options['server_ip'] = server_addr[0]

    if len(server_addr) == 1:
      logging.debug('Defaulting to server port {0} !'.format(DEFAULT_SERVER_PORT))
      options['server_port'] = DEFAULT_SERVER_PORT
    else:
      options['server_port'] = server_addr[1]

  else:
    logging.debug('Defaulting to server {0}:{1} !'.format(LOCALHOST_IP, DEFAULT_SERVER_PORT))
    options['server_ip'] = LOCALHOST_IP
    options['server_port'] = DEFAULT_SERVER_PORT

  if options['port'] is None:
    options['port'] = DEFAULT_CLIENT_PORT

  return options

def main(params):
  options = parse_options(params)
  client = Client(options)
  client.start()

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  main(sys.argv[1:])