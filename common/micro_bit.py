from common.communication import RadioClient

class Stack:
    """
    Generates object, that will classify by an importance the tasks
    """

    def __init__(self):
        self.stack = []

    def __getitem__(self, i):
        return self.stack.pop(i)

    def apend(self, item):
        self.stack.append(item)

class Micro_Bit_Client:

    message_types = {}
    tasks = []

    def __init__(self):
        self.stack = []
        self.radio_client = RadioClient()

    def add_received_task(self):
        message_type, message_data = self.radio_client.get_message()

        if message_type:
            func = self.message_types[message_type]
            func_with_args = (func, message_data)
    
            self.stack.append(func_with_args)

    def check_self_tasks(self):
        for task in self.tasks:
            task(self)

    def update_stack(self):
        self.add_received_task()
        self.check_self_tasks()

    def update(self):
        self.update_stack()
        if self.stack:
            self.stack[-1][0](self.stack[-1][1])

    def run(self):
        while True:
            self.update()
