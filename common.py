import struct
import logging
import urllib2
import sys

GET_PUBLIC_IP_URL = 'http://ip.42.pl/raw'
LOCALHOST_IP = '127.0.0.1'
DEFAULT_CLIENT_PORT = 11111
DEFAULT_SERVER_PORT = 50000

def get_public_ip():
  '''Get external public ip'''
  try:
    ip = urllib2.urlopen(GET_PUBLIC_IP_URL).read()
  except:
    logging.error(sys.exc_info())
    logging.error('Failed to query external server to get my public ip! Defaulting to 127.0.0.1')
    ip = '127.0.0.1'
  return ip

def send_message(socket, message):
  '''Prefix each message with a 4-byte length (network byte order)'''
  message = struct.pack('>I', len(message)) + message
  socket.sendall(message)

def recv_message(socket):
  '''Read message length and unpack it into an integer'''
  raw_message_len = __recv_all(socket, 4)
  if not raw_message_len:
    return None

  message_len = struct.unpack('>I', raw_message_len)[0]

  # Read the message data
  return __recv_all(socket, message_len)

def __recv_all(socket, num_bytes):
  '''Helper function to recv num_bytes bytes or return None if EOF is hit'''
  data = ''
  while len(data) < num_bytes:
    packet = socket.recv(num_bytes - len(data))
    if not packet:
      return None
    data += packet
  return data