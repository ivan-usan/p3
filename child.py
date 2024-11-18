from common.micro_bit import Micro_Bit_Client

class Child_Micro_Bit_Client(Micro_Bit_Client):

    """
    Detector notifying agent in 2 of 3 functions to do (lumisinoty, movements)
    - Get reactions of other agent -> represent them straightaway
    - Inform other agents about current events -> do after, showing reactions
      Save information of done events -> few time spans, that are required to not span parent.

    Information provider in 1/3 functions (milk)
    - provide info about current level

    Interface executor in 1/3 functions (milk)
    - change setting that are related to milk
    """

    def __init__(self):
        super().__init__()

        self.self_tasks = [self.check_mouvement]
    
    def detect_mouvement(self):
        get_values() 
        def set_range (values): 
            if accelerometer.set_range (8):
                accelerometer.is_gesture ("freefall") 
            elif acceleromater.set_range(4):
                accelerometer.is_gesture ("shake")
            else :
                accelerometer. is_gesture("face down") 

    def notify_mouvement(self):
        pass

    prev_mouvement = None
    def check_mouvement(self):
        mouvement = self.detect_mouvement()
        if prev_mouvement != mouvement:
            if mouvement == '': # add other conditions
                self.notify_mouvement()

            prev_mouvement = movement

    def apply_mouvement_reaction(self, reaction):
        """

        The event function is more important than notifying about current dectection.

        Args:
            reaction - :str either music or image
        """
        pass


    milk_level = 0
    def show_milk(self):
        pass

    def milk_menu(self):
        pass

    def send_milk_level(self):
        pass

    def give_milk(self):
        pass

    def reduce_milk(self):
        pass

    def reset_milk_level(self):
        pass

child_micro_bit = Child_Micro_Bit_Client()
child_micro_bit.run()
