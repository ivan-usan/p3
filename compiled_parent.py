

class Micro_Bit_Client:

    message_types = {}
    tasks = []

    def __init__(self):
        self.stack = []
        self.radio_client = RadioClient()

    def add_received_task(self):
        message_type, message_data = self.radio_client.get_message()

        cond = message_type and message_type != 1 and message_type in self.message_types
        # if message_type:
        #     display.show(str(message_type))
        #     sleep(500)

        if cond:
            func = self.message_types[message_type]
    
            if not message_data:
                self.stack.append(func)
            else:
                self.stack.append((func, message_data))

    def check_tasks(self):
        for task in self.tasks:
            task()

    def update_stack(self):
        self.check_tasks()
        self.add_received_task()

    def update(self):
        self.update_stack()
        if self.stack:
            task = self.stack[-1]

            if isinstance(self.stack[-1], tuple):
                self.stack.pop(-1)
                # display.scroll('executed')
                # sleep(1000)

                task[0](task[1])

            else:
                # display.scroll('not tuple')
                # sleep(500)

                is_continue = task() # only menus can return True
                if not is_continue:
                    self.stack.pop(-1)
                    display.clear()

            sleep(500)

    def run(self):
        while True:
            try:
                self.update()
            except:
                continue

from microbit import *

import random
import radio

radio.config(group=244, channel=44, address=0x11111122)
radio.on()
password = 'monolisa'

# seed to put random.seed(:int)
def hashing(string):
	"""
	Hachage d'une chaÃ®ne de caractÃ¨res fournie en paramÃ¨tre.
	Le rÃ©sultat est une chaÃ®ne de caractÃ¨res.
	Attention : cette technique de hachage n'est pas suffisante (hachage dit cryptographique) pour une utilisation en dehors du cours.

	:param (str) string: la chaÃ®ne de caractÃ¨res Ã  hacher
	:return (str): le rÃ©sultat du hachage
	"""

	def to_32(value):
		"""
		Fonction interne utilisÃ©e par hashing.
		Convertit une valeur en un entier signÃ© de 32 bits.
		Si 'value' est un entier plus grand que 2 ** 31, il sera tronquÃ©.

		:param (int) value: valeur du caractÃ¨re transformÃ© par la valeur de hachage de cette itÃ©ration
		:return (int): entier signÃ© de 32 bits reprÃ©sentant 'value'
		"""
		value = value % (2 ** 32)
		if value >= 2**31:
			value = value - 2 ** 32
		value = int(value)
		return value

	if string:
		x = ord(string[0]) << 7
		m = 1000003
		for c in string:
			x = to_32((x*m) ^ ord(c))
		x ^= len(string)
		if x == -1:
			x = -2
		return str(x)
	return ""

def vigenere(message, key, decryption=False):
    text = ""
    key_length = len(key)
    key_as_int = [ord(k) for k in key]

    for i, char in enumerate(str(message)):
        #Letters encryption/decryption
        if char.isalpha():
            key_index = i % key_length
            if decryption:
                modified_char = chr((ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord('A'))
            else : 
                modified_char = chr((ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord('A'))
            #Put back in lower case if it was
            if char.islower():
                modified_char = modified_char.lower()
            text += modified_char
        #Digits encryption/decryption
        elif char.isdigit():
            key_index = i % key_length
            if decryption:
                modified_char = str((int(char) - key_as_int[key_index]) % 10)
            else:  
                modified_char = str((int(char) + key_as_int[key_index]) % 10)
            text += modified_char
        else:
            text += char
    return text

class RadioClient:

    nonce = 1

    def __init__(self):
        self.state_connection = 'connecting' # connected
        self.nonce_set = set()

        self.password = password

        self.challenge = random.random() # in case of child
        self.set_up_challenge(self.challenge)
    

    def send_message(self, message_type, message_data=''):
        """
        Args:
            message_type - :str, represents message's type
            message_data - :str, represents message data
        """

        message_data = str(self.nonce) + ':' + message_data
        message_data = vigenere(message_data, self.password)

        self.nonce_set.add(self.nonce)
        self.nonce += 1

        message = '|'.join([str(message_type), str(len(message_data)), message_data])
        radio.send(message)

    def get_message(self):
        """
        Returns: message type and message data
        """
        try:
            message = radio.receive()
    
            if not message:
                return None, None
    
            message_type, message_length, message_data = message.split('|')
            message_data = vigenere(message_data, self.password, decryption=True)
    
            nonce, message_data = message_data.split(':')
    
            if nonce in self.nonce_set:
                return None, None
            else:
                self.nonce_set.add(int(nonce))
                self.nonce = int(nonce)+1
    
            return int(message_type), message_data
        except:
            return None, None

    def set_up_challenge(self, challenge_seed):
        random.seed(int(challenge_seed*10**7))

    def connect_to_parent(self):
        if self.state_connection == 'connected':
            display.show('-')
            return True

        elif self.state_connection == 'connecting':
            message_type, message_data = self.get_message()

            if message_type == 0x02:
                display.show(Image.DIAMOND)

                new_challenge = random.random()
                challenge_hash = hashing(str(new_challenge))

                if message_data == challenge_hash:
    
                    self.password = self.password + str(new_challenge)
                    self.state_connection = 'connected'
            else:
                display.show('.')

                self.send_message(str(0x01), str(self.challenge))

    def connect_to_child(self):
        if self.state_connection == 'connected':
            display.show('-')
            return True

        elif self.state_connection == 'connecting':
            display.show('.')

            message_type, message_data = self.get_message()

            if message_type == 0x01:
                display.show(Image.DIAMOND)

                challenge = float(message_data)
                self.set_up_challenge(challenge)

                new_challenge = random.random()
                challenge_hash = hashing(str(new_challenge))

                self.send_message(0x02, challenge_hash)
                self.state_connection = 'connected'


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
    
    def handle_luminosity_change(self, luminosity):
        if luminosity == 'Day':
            display.show(Image.ALL_CLOCKS[:7])

        elif luminosity == 'Night':
            display.show(list(Image.ALL_CLOCKS[6:])+[Image.ALL_CLOCKS[0]])

        sleep(1000)

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
        
    def handle_mouvement_change(self, mouvement):
        #if mouvement == 'agité':
        #    display.show(Image.SURPRISED)
#
        # if mouvement == 'très agité':
        display.show(Image.ANGRY)
        sleep(1000)
        self.stack.append(self.mouvement_menu)
    
    def mouvement_menu(self):
        if button_a.is_pressed():
            task = 'image'
            if self.curr_mouvement_option == 0: # music
                task = 'music'
            self.radio_client.send_message(4, task)

            return False

        elif button_b.is_pressed():
            self.curr_mouvement_option += 1
            self.curr_mouvement_option = self.curr_mouvement_option % 2

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
            # display.scroll("sent")
            # sleep(300)

        elif button_b.is_pressed():
            self.curr_milk_option = (self.curr_milk_option+1) % 4
            # display.scroll(str(self.curr_milk_option))
            # sleep(300)

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
