messages_types = [
    # key - :int in hex format of max size 32 bytes:
    # value - :function 
    0x01 # connection method    
]

import json

# function to use json.loads, json.dumps

import random

# seed to put random.seed(:int)

class RadioClient:

    def __init__(self):
        self.state_connection = 'connecting' # waiting, connected
        # self.micro_bit_client = micro_bit_client

    def send_message(self, message_type, message_data):
        """
        Args:
            message_type - :str, represents message's type
            message_data - :str, represents message data
        """
        pass

    def get_message(self):
        """
        Returns: message type and message data
        """
        message_type, message_data = ..., ...
        return message_type, message_data

    def connect_to_parent(self):
        if self.state_connection == 'connected':
            return True
        

    def connect_to_child(self):
        pass
