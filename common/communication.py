messages_types = [
    # key - :int in hex format of max size 32 bytes:
    # value - :function 
    0x01 # connection method    
]

class RadioClient:

    def __init__(self):
        pass
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
