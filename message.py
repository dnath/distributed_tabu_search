import json
from enum import IntEnum

class MessageTypes(IntEnum):
  GET_SEED = 1
  PUT_SEED = 2

class MessageError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class Message:
  def __init__(self, options):
    if not options.has_key('message_type') or not isinstance(options['message_type'], MessageTypes):
      raise MessageError('Invalid Message! params = {0}'.format(options))

    self.sender_ip = options['sender_ip']
    self.sender_port = options['sender_port']

    self.receiver_ip = options['receiver_ip']
    self.receiver_port = options['receiver_port']

    self.message_type = options['message_type']
    self.message = options['message']

  def serialize(self):
    '''Serialize into a json string'''
    return json.dumps(self, cls=MessageEncoder)

  def __str__(self):
    return str(self.serialize())

  @staticmethod
  def deserialize(json_string):
    '''Deserialize from a json string''' 
    json_message_obj = json.loads(json_string)
    if not json_message_obj.has_key('message_type'):
      raise MessageError('No Message Type! Cannot deserialize json_string = {0}'.format(json_string))
    
    json_message_obj['message_type'] = MessageTypes(json_message_obj['message_type'])
    return Message(options=json_message_obj)

class MessageEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Message):
      var_dict = vars(obj)
      var_dict['message_type'] = var_dict['message_type'].value

      res = dict(type=obj.__class__.__name__)
      res.update(var_dict)
      return res

    return json.JSONEncoder.default(self, obj)

