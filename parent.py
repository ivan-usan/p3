from common.micro_bit import Micro_Bit_Client
import time
import radio

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
        self.curr_mouvement_option = 0
        self.curr_milk_option = 0

        self.message_types = {
            3: self.handle_mouvement_change,
            5: self.handle_luminosity_change,
            7: self.show_milk_level,
        }

        self.stack = [self.milk_menu]
        self.stack_indexes = [-1]
    
    def handle_luminosity_change(self, luminosity):
        if self.stack_indexes[-1] == -2:
            return

        if luminosity == 'Day':
            display.show(Image.ALL_CLOCKS[:7])

        elif luminosity == 'Night':
            display.show(list(Image.ALL_CLOCKS[6:])+[Image.ALL_CLOCKS[0]])

        sleep(1000)

        self.stack_append(-2, self.luminosity_menu)

    def luminosity_menu(self):
        if button_a.is_pressed():
            if self.curr_luminosity_option == 0: # music
                task = 'music'
            else: # image
                task = 'image'

            self.radio_client.send_message(6, task)
            display.show(['-', Image.ARROW_E])

            return False

        elif button_b.is_pressed():
            self.curr_luminosity_option += 1
            self.curr_luminosity_option = self.curr_luminosity_option % 2
            sleep(500)

        else:
            if self.curr_luminosity_option == 0: # music
                image = Image.MUSIC_QUAVER
            else: # image
                image = Image.GHOST

            display.show(image)

        return True
        
    def handle_mouvement_change(self, mouvement):
        if self.stack_indexes[-1] == -3:
            return

        display.show([Image.ARROW_E, Image.ARROW_W])
        sleep(500)

        self.stack_append(-3, self.mouvement_menu)
    
    def mouvement_menu(self):
        if button_a.is_pressed():
            task = 'image'
            if self.curr_mouvement_option == 0: # music
                task = 'music'
            self.radio_client.send_message(4, task)
            display.show(['-', Image.ARROW_E])

            return False

        elif button_b.is_pressed():
            self.curr_mouvement_option += 1
            self.curr_mouvement_option = self.curr_mouvement_option % 2
            sleep(500)

        else:
            if self.curr_mouvement_option == 0: # music
                # image = Image.MUSIC
                image = Image.MUSIC_QUAVER
            else: # image
                # image = Image.BUTTERFLY
                image = Image.GHOST

            display.show(image)

        return True

    def run(self):
        display.show('P')
        sleep(1000)

        while not self.radio_client.connect_to_child():
            sleep(100)

        super().run()

    def show_milk_level(self, milk_level):
        display.scroll(str(milk_level))

    def milk_menu(self):
        """
        4 options:
        - increase milk level
        - reduce milk level
        - show milk level
        - make milk level to 0
        """

        if button_a.is_pressed():
            if self.curr_milk_option == 0: # milk level
                task = '?'
            elif self.curr_milk_option == 1: # increase 
                task = '->'
            elif self.curr_milk_option == 2: # reduce
                task = '<-'
            else:
                task = '0'

            self.radio_client.send_message(8, task)
            display.show(['-', Image.ARROW_E])
            self.curr_milk_option = 0

        elif button_b.is_pressed():
            self.curr_milk_option = (self.curr_milk_option+1) % 4
            sleep(500)

        else:
            if self.curr_milk_option == 0: # milk level
                image = '?'

            elif self.curr_milk_option == 1: # increase
                image = Image.ARROW_N

            elif self.curr_milk_option == 2: # reduce
                image = Image.ARROW_S

            elif self.curr_milk_option == 3: # 0
                image = '=0'

            display.show(image)

        return True
    
parent_micro_bit = Parent_Micro_Bit_Client()
parent_micro_bit.run()
