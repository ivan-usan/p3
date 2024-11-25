messages_types = [
    # key - :int in hex format of max size 32 bytes:
    # value - :function 
    0x01 # connection method    
]

import radio

radio.on()

import json

import random

# seed to put random.seed(:int)
def hashing(string):
	"""
	Hachage d'une chaîne de caractères fournie en paramètre.
	Le résultat est une chaîne de caractères.
	Attention : cette technique de hachage n'est pas suffisante (hachage dit cryptographique) pour une utilisation en dehors du cours.

	:param (str) string: la chaîne de caractères à hacher
	:return (str): le résultat du hachage
	"""

	def to_32(value):
		"""
		Fonction interne utilisée par hashing.
		Convertit une valeur en un entier signé de 32 bits.
		Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.

		:param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
		:return (int): entier signé de 32 bits représentant 'value'
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

    state_connection = 'searching'
    nonce = 1

    def __init__(self):
        self.state_connection = 'connecting' # waiting, connected
        self.nonce_set = set()

        with open('common/password.txt') as f:
            self.password = f.read()

    def send_message(self, message_type, message_data):
        """
        Args:
            message_type - :str, represents message's type
            message_data - :str, represents message data
        """
        message_data = f'{self.nonce}:{message_data}'
        message_data = vigenere(message_data, self.password)

        self.nonce_set.add(self.nonce)
        self.nonce += 1

        radio.send(f'{message_type}|{len(message_data)}|{message_data}')

    def get_message(self):
        """
        Returns: message type and message data
        """
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

        return message_type, message_data

    def set_up_challenge(self, challenge_seed):
        random.seed(challenge_seed)

    def connect_to_parent(self):
        if self.state_connection == 'connected':
            return True
        elif self.state_connection == 'connecting':
            new_challenge = random.random()
            challenge_hash = hashing(str(new_challenge))

            message_type, calculated_hash = self.get_message()

            if calculated_hash == challenge_hash:
                self.password = self.password + str(new_challenge)
                self.state_connection = 'connected'

        elif self.state_connection == 'searching':
            challenge = random.random()
            self.set_up_challenge(challenge)

            self.send_message(str(0x01), f'{challenge}')
            self.state_connection = 'connecting'

    def connect_to_child(self):
        if self.state_connection == 'connected':
            return True
        elif self.state_connection == 'searching':
            message_type, message_data = self.get_message()

            if message_type == str(0x01):
                nonce,challenge = [int(value) for value in message_data.split(' ')]
                self.set_up_challenge(challenge)

                new_challenge = random.random()
                challenge_hash = hashing(str(new_challenge))

                self.send_message(0x02, challenge_hash)

                self.state_connection = 'connected'
