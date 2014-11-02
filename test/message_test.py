import unittest
from message import *

class TestMessage(unittest.TestCase):
  def test_serialize(self):
    msg_options = { 'sender_ip': '1.2.3.4',
                    'sender_port': 1234,
                    'receiver_ip': '11.22.33.44',
                    'receiver_port': 9999,
                    'message_type': MessageTypes.GET_SEED,
                    'message': '' }

    message = Message(msg_options)
    msg = '{"sender_port": 1234, "receiver_ip": "11.22.33.44", "receiver_port": 9999, "sender_ip": "1.2.3.4", "message_type": 1, "message": "", "type": "Message"}'
    
    self.assertEqual(message.serialize(), msg)

  def test_deserialize(self):
    self.assertRaises(MessageError, Message.deserialize, '{}')
    self.assertRaises(ValueError, Message.deserialize, '{"message_type":40000}')

    json_string = '{"sender_port": 1234, "receiver_ip": "11.22.33.44", "receiver_port": 9999, "sender_ip": "1.2.3.4", "message_type": 1, "message": "", "type": "Message"}'
    msg = Message.deserialize(json_string)
    self.assertDictEqual(vars(msg),
                         {'sender_ip': '1.2.3.4',
                          'sender_port': 1234,
                          'receiver_ip': '11.22.33.44',
                          'receiver_port': 9999,
                          'message_type': MessageTypes.GET_SEED,
                          'message': '' })

if __name__ == '__main__':
  unittest.main()