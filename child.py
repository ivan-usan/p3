from micro : bit import Micro:Bit_Client
from microbit import accelerometer, display, button_a, button_b, music

class Child_MicroBit_Client(Micro:Bit_Client):
    """
    Cette classe représente un client micro:bit pour l'enfant. Elle gère la détection des mouvements,
    les notifications envoyées au parent, et la gestion de la quantité de lait.
    """

    def __init__(self):
        super().__init__()

        # Initialisation de l'état précédent du mouvement et du niveau de lait
        self.prev_mouvement = None
        self.milk_level = 0  # Quantité de lait initiale

        # Liste des tâches à exécuter pour cet agent
        self.self_tasks = [self.check_mouvement, self.show_milk]

    def detect_mouvement(self):
        """
        Détecte les mouvements de l'enfant en utilisant l'accéléromètre.
        Retourne un état de mouvement : "endormi", "agité", ou "très agité".
        """
        get_values()
        def set_ranges (values):

        # Seuils à ajuster selon les besoins pour détecter les mouvements
            if accelerometer.set_range(8):
                accelerometer.is_gesture("freefall")
                return "très agité"
        
            elif accelerometer.set_range(4):
                accelerometer.is_gesture("shake")
                return "agité"
            else : 
                return "endormi"

    def notify_mouvement(self, mouvement):
        """
        Notifie le parent en fonction de l'état du mouvement de l'enfant.
        """
        self.radio_client.send_message(0x02, {})
        
    def check_mouvement(self):
        """
        Vérifie si le mouvement de l'enfant a changé et notifie le parent.
        """
        current_mouvement = self.detect_mouvement()
        if self.prev_mouvement != current_mouvement:
            self.notify_mouvement(current_mouvement)
            self.prev_mouvement = current_mouvement

    def apply_mouvement_reaction(self, reaction):
        """
        Applique une réaction au mouvement : musique ou image.
        """
        if reaction == "musique":
            music.play(music.POWER_UP)
        elif reaction == "image":
            display.show("Z")  # Image représentant le bébé en sommeil

    # Fonctions liées à la gestion de la quantité de lait

    def show_milk(self):
        """
        Affiche le niveau actuel de lait sur l'écran LED.
        """
        display.show(str(self.milk_level))

    def milk_menu(self):
        """
        Menu pour gérer la quantité de lait via les boutons A et B.
        Le bouton A permet d'ajouter du lait, et le bouton B de retirer du lait.
        """
        if button_a.is_pressed():
            self.give_milk()
        elif button_b.is_pressed():
            self.reduce_milk()

    def send_milk_level(self):
        """
        Envoie le niveau de lait actuel au parent.
        Ce message pourrait être envoyé via Bluetooth ou une autre méthode de communication.
        """
        message = f"3|{len(str(self.milk_level))}|{self.milk_level}"
        self.send_message(message)

    def give_milk(self):
        """
        Augmente la quantité de lait consommée.
        """
        if self.milk_level < 10:  # Limite du niveau de lait, ajustable
            self.milk_level += 1
        self.show_milk()

    def reduce_milk(self):
        """
        Réduit la quantité de lait consommée.
        """
        if self.milk_level > 0:
            self.milk_level -= 1
        self.show_milk()

    def reset_milk_level(self):
        """
        Réinitialise la quantité de lait consommée à zéro.
        """
        self.milk_level = 0
        self.show_milk()

# Création de l'instance du micro:bit enfant
child_micro_bit = Child_Micro_Bit_Client()
child_micro:bit.run()  # Lancer l'exécution des tâches
