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
        self.curr_luminosity_option = 0
        self.stage = []
        self.stage_len = 225

        self.is_day_level_set_up = False
        self.day_level = None

        # Liste des tâches à exécuter pour cet agent

        self.tasks = [self.check_luminosity, self.check_mouvement]
        self.stack = [self.milk_menu, self.set_up_luminosity_level, ]
        self.stack_indexes = [-1, -2, ]

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

        sleep(1000)

    # Fonctions liées à la gestion de la quantité de lait
    def show_milk_level(self):
        """
        Affiche le niveau actuel de lait sur l'écran LED.
        """
        display.scroll(str(self.milk_level))
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
        display.scroll(task)
        if task == '?':
            self.send_milk_level()

        elif task == '0':
            self.milk_level = 0

        elif task == '->':
            self.milk_level += 1

        elif task == '<-' and self.milk_level > 0:
            self.milk_level -= 1

    def set_up_luminosity_level(self):
        if not self.day_level:
            self.day_level = display.read_light_level()

            display.scroll("L%: "+str(self.day_level))
            sleep(1000)

        if button_a.is_pressed():
            if self.curr_luminosity_option == 0: # luminosity level
                self.is_day_level_set_up = True

                return False

            elif self.curr_luminosity_option == 1: # luminosity level
                display.scroll(str(self.day_level))
                sleep(1000)

            elif self.curr_luminosity_option == 2: # increase 
                self.day_level += 10

            elif self.curr_luminosity_option == 3: # reduce
                self.day_level -= 10

            if self.curr_luminosity_option > 1:
                display.show(['-', Image.ARROW_E])

        elif button_b.is_pressed():
            self.curr_luminosity_option = (self.curr_luminosity_option+1) % 4
            sleep(500)

        else:
            if self.curr_luminosity_option == 0: # luminosity level
                image = 'O'

            elif self.curr_luminosity_option == 1: # increase
                image = '?'

            elif self.curr_luminosity_option == 2: # reduce
                image = Image.ARROW_N

            elif self.curr_luminosity_option == 3: # 0
                image = Image.ARROW_S

            display.show(image)

        return True

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
        if len(self.stage) < self.stage_len:
            self.stage.append(display.read_light_level())

            if not self.is_day_level_set_up:
                self.stage = self.stage[1:]

            if len(self.stage) == self.stage_len:
                self.luminosity = self.get_luminosity()
        else:
            self.stage = self.stage[1:]
            self.stage.append(display.read_light_level())

            # dipslay.scroll(str(self.luminosity_degree()))
            # sleep(200)

            curr_luminosity = self.get_luminosity()
            if curr_luminosity != self.luminosity:
                self.luminosity = curr_luminosity
                self.radio_client.send_message(5, self.luminosity)

        
    def get_luminosity(self):
        if self.luminosity_degree() > self.day_level:
            return "Day"
        else:
            return "Night"
        
    def luminosity_degree(self):
        degree = sum(self.stage) / self.stage_len
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
