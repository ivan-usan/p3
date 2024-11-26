from common.micro_bit import Micro_Bit_Client
import time

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

        self.curr_luminosity_option = 0

        self.message_types = {
            5: self.handle_luminosity_change
        }
    
    def show_detected_mouvement(self):
        pass

    def handle_detected_mouvement(self):
        """
        changes the current state and 
        """
        pass
    
    def handle_luminosity_change(self, luminosity):
        if luminosity == 'Day':
            display.show(Image.ALL_CLOCKS[:7])

        elif luminosity == 'Night':
            display.show(list(Image.ALL_CLOCKS[6:])+[Image.ALL_CLOCKS[0]])

        self.stack.append(self.luminosity_menu)

    def luminosity_menu(self):
        if button_a.is_pressed():
            if self.curr_luminosity_option == 0: # music
                task = 'music'
            else: # image
                task = 'image'

            self.radio_client.send_message(6, task)

            return False

        elif button_b.is_pressed():
            self.curr_luminosity_option += 1
            self.curr_luminosity_option = self.curr_luminosity_option % 2

        else:
            if self.curr_luminosity_option == 0: # music
                image = Image.MUSIC_QUAVER
            else: # image
                image = Image.GHOST

            display.show(image)

        return True

    def run(self):
        while not self.radio_client.connect_to_child():
            sleep(100)

        super().run()

parent_micro_bit = Parent_Micro_Bit_Client()
parent_micro_bit.run()
