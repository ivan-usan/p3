

class Micro_Bit_Client:

    message_types = {}
    tasks = []
    stack_indexes = []

    def __init__(self):
        self.stack = []
        self.radio_client = RadioClient()

    def add_received_task(self):
        message_type, message_data = self.radio_client.get_message()

        # if message_type and message_type != 1:
        #     display.show(message_type)
        #     sleep(1000)

        if message_type and message_type != 1 and message_type in self.message_types:
            func = self.message_types[message_type]
    
            if not message_data:
                data = func
            else:
                data = (func, message_data)

            self.stack_append(message_type, data)

    def check_tasks(self):
        for task in self.tasks:
            task()

    def update_stack(self):
        self.check_tasks()
        self.add_received_task()

    def stack_append(self, message_type, data):
        # display.scroll(str(message_type)+str(self.stack_indexes))
        # sleep(2500)
            
        if message_type in self.stack_indexes:
            # display.scroll('skip'), sleep(1000)
            index = self.stack_indexes.index(message_type)
            self.stack_pop(index)

        self.stack_indexes.append(message_type)
        self.stack.append(data)

    def stack_pop(self, index):
        self.stack_indexes.pop(index)
        self.stack.pop(index)

    def update(self):
        self.update_stack()
        if self.stack:
            task = self.stack[-1]

            if isinstance(self.stack[-1], tuple):
                self.stack_pop(-1)

                task[0](task[1])

            else:
                is_continue = task() # only menus can return True
                if not is_continue:
                    self.stack_pop(-1)
                    display.clear()

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

from microbit import *


import music
import time
import math

class Child_Micro_Bit_Client(Micro_Bit_Client):
    """
    Cette classe représente un client micro:bit pour l'enfant. Elle gère la détection des mouvements,
    les notifications envoyées au parent, et la gestion de la quantité de lait.
    """
    def __init__(self):
        super().__init__()
        # Initialisation de l'état précédent du mouvement et du niveau de lait
        self.prev_mouvement = None
        self.milk_level = 0 # Quantité de lait initiale
        self.stage = []
        self.luminosity = " "
        # Liste des tâches à exécuter pour cet agent

        self.tasks = [self.check_luminosity, self.check_mouvement]
        self.stack = [self.milk_menu, ]
        self.stack_indexes = [-1, ]

        self.message_types = {
            4: self.apply_mouvement_reaction,
            6: self.luminosity_react,
            8: self.milk_menu_react
        }

    def detect_mouvement(self):
        """
        Détecte les mouvements de l'enfant en utilisant l'accéléromètre.
        Retourne un état de mouvement : "endormi", "agité", ou "très agité".
        """
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        
        distance = math.sqrt((x)**2+(y)**2+(z)**2)
        if distance >= 2500:
            return "très agité"
    
        elif distance < 2500 and distance >= 700 :
            return "agité"
        
        else : 
            return "endormi"

    def notify_mouvement(self, mouvement):
        """
        Notifie le parent en fonction de l'état du mouvement de l'enfant.
        """
        # display.scroll('notified')
        self.radio_client.send_message(3, 'some')
        
    def check_mouvement(self):
        """
        Vérifie si le mouvement de l'enfant a changé et notifie le parent.
        """
        current_mouvement = self.detect_mouvement()
        if self.prev_mouvement != current_mouvement:
            if current_mouvement == "très agité":
                self.notify_mouvement(current_mouvement)
            self.prev_mouvement = current_mouvement

    def apply_mouvement_reaction(self, reaction):
        """
        Applique une réaction au mouvement : musique ou image.
        """
        # display.show('application')
        if reaction == "music":
            music.play(music.POWER_UP)
        elif reaction == "image":
            display.show("Z")  # Image représentant le bébé en sommeil

        sleep(500)

    # Fonctions liées à la gestion de la quantité de lait
    def show_milk_level(self):
        """
        Affiche le niveau actuel de lait sur l'écran LED.
        """
        display.scroll(str(self.milk_level))
        sleep(500)

    def milk_menu(self):
        """
        Menu pour gérer la quantité de lait via les boutons A et B.
        Le bouton A permet d'ajouter du lait, et le bouton B de retirer du lait.
        """
        if button_a.is_pressed():
            self.show_milk_level()
        else:
            display.show('?')

        return True

    def milk_menu_react(self, task):
        display.scroll(task)
        if task == '?':
            self.send_milk_level()
        elif task == '0':
            self.milk_level = 0
        elif task == '->':
            self.milk_level += 1
        elif task == '<-' and self.milk_level > 0:
            self.milk_level -= 1

    def send_milk_level(self):
        """
        Envoie le niveau de lait actuel au parent.
        Ce message pourrait être envoyé via Bluetooth ou une autre méthode de communication.
        """
        message = str(self.milk_level)
        self.radio_client.send_message(7, message)

    def check_luminosity(self):
        """
        Vérifie si la luminosité de la pièce a changé et notifie le parent.
        """
        if len(self.stage) < 5:
            self.stage.append(display.read_light_level())
            self.luminosity = self.get_luminosity()
        else:
            self.stage = self.stage[1:]
            self.stage.append(display.read_light_level())

        if len(self.stage) == 5:
            curr_luminosity = self.get_luminosity()
            if curr_luminosity != self.luminosity:

                self.luminosity = curr_luminosity
                self.radio_client.send_message(5, self.luminosity)

        
    def get_luminosity(self):
        #luminosity = display.read_light_level()
        # display.scroll(str(self.luminosity_degree()))
        # sleep(800)
        if self.luminosity_degree() > 75:
            return "Day"
        else:
            return "Night"
        
    def luminosity_degree(self):
        degree = sum(self.stage) / 5
        return degree
    
    def luminosity_react(self, react):
        if react == "music":
            music.play(music.POWER_UP)
        elif react == "image":
            display.show("Z") 

        sleep(500)
 
    def run(self):
        display.show('E')
        sleep(1000)

        while not self.radio_client.connect_to_parent():
            sleep(100)

        super().run()
    
# Création de l'instance du micro:bit enfant
child_micro_bit = Child_Micro_Bit_Client()
child_micro_bit.run()  # Lancer l'exécution des tâches
