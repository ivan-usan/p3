from microbit import *
from common.micro_bit import Micro_Bit_Client

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
        if distance >= 2000:
            return "très agité"
    
        elif distance < 2000 and distance >= 700 :
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

        sleep(1000)

    # Fonctions liées à la gestion de la quantité de lait
    def show_milk_level(self):
        """
        Affiche le niveau actuel de lait sur l'écran LED.
        """
        display.show(str(self.milk_level))
        sleep(1000)

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

        if self.luminosity == " ":
            luminosity = display.read_light_level()
            if luminosity > 25:
                self.luminosity = "Day"
            else:
                self.luminosity = "Night"

        elif len(self.stage) == 5:
            curr_luminosity = self.get_luminosity()
            if curr_luminosity != self.luminosity:

                self.luminosity = curr_luminosity
                self.radio_client.send_message(5, self.luminosity)

            self.stage = self.stage[1:]

        self.stage.append(display.read_light_level())
        
    def get_luminosity(self):
        #luminosity = display.read_light_level()
        if self.luminosity_degree() > 25:
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

        sleep(1000)
 
    def run(self):
        display.show('E')
        sleep(1000)

        while not self.radio_client.connect_to_parent():
            sleep(100)

        super().run()
    
# Création de l'instance du micro:bit enfant
child_micro_bit = Child_Micro_Bit_Client()
child_micro_bit.run()  # Lancer l'exécution des tâches
