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
        
    def handle_mouvement_change(self, mouvement):
        if mouvement == 'agité':
            display.show(Image.SURPRISED)

        elif luminosity == 'très agité':
            display.show(Image.ANGRY)

        self.stack.append(self.mouvement_menu)
    
    def mouvement_menu(self):
        if button_a.is_pressed():
            if self.curr_mouvement == 0: # music
                task = 'music'
            self.radio_client.send_message(6, task)

            return False

        elif button_b.is_pressed():
            self.curr_mouvement_option += 1
            self.curr_mouvement_option = self.curr_mouvement_option % 2

        else:
            if self.curr_mouvement_option == 0: # music
                image = Image.DUCK
            else: # image
                image = Image.BUTTERFLY

            display.show(image)

        return True
    def run(self):
        while not self.radio_client.connect_to_child():
            sleep(100)

        super().run()

    Initialiser le radio pour la communication
    radio.on()
    radio.config(channel=19)  # Choisir un canal pour la communication BLE
    
    Initialisation de la quantité de lait
    quantite_lait = 0
    
    def envoyer_message(message):
        """Envoie un message via le radio"""
        radio.send(message)
    
    def afficher_quantite_lait():
        """Affiche la quantité de lait sur l'écran LED"""
        if quantite_lait == 0:
            display.show(Image.NO)
        else:
            display.scroll(str(quantite_lait))
    
    while True:
        if button_a.is_pressed():  # Ajout d'une dose de lait
            quantite_lait += 1
            envoyer_message("Dose de lait ajoutée")
            sleep(500)
    
        if button_b.is_pressed():  # Suppression d'une dose erronée
            if quantite_lait > 0:
                quantite_lait -= 1
                envoyer_message("Dose de lait supprimée")
            sleep(500)
    
        if pin_logo.is_touched():  # Réinitialisation de la quantité de lait à zéro
            quantite_lait = 0
            envoyer_message("Quantité de lait réinitialisée")
            sleep(500)
    
        # Affichage de la quantité de lait
        afficher_quantite_lait()
    
    Affichage des informations reçues du be:bi' enfant
        message_recu = radio.receive()
        if message_recu:
            display.scroll(message_recu)
    
    parent_micro_bit = Parent_Micro_Bit_Client()
    parent_micro_bit.run()
