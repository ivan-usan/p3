from common.micro_bit import Micro_Bit_Client

class Parent_Micro_Bit_Client(Micro_Bit_Client):

    """
    Reactions-Decisions maker agent in 2 of 3 functions to do (lumisinoty, movements)
    - Notify about events with other agent -> inform about current actions to do (inform straightaway by fast signal)
    - Giving the possibility to make decision -> wait until decision (create a menu for functions menus)

    Decisions makers agent in 1 of 3 functions - Interface provider
    - Select actions
    - Get info about current level
    """

    def __init__(self):
        super().__init__()

        self.message_types = {

        }
    
    def show_detected_mouvement(self):
        pass

    def handle_detected_mouvement(self):
        """
        changes the current state and 
        """
        pass

parent_micro_bit = Parent_Micro_Bit_Client()
parent_micro_bit.run()
