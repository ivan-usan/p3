from common.communication import RadioClient

class Micro_Bit_Client:

    message_types = {}
    tasks = []

    def __init__(self):
        self.stack = []
        self.radio_client = RadioClient()

    def add_received_task(self):
        message_type, message_data = self.radio_client.get_message()

        if message_type and message_type != 1 and message_type in self.message_types:
            func = self.message_types[message_type]
    
            if not message_data:
                self.stack.append(func)
            else:
                self.stack.append((func, message_data))

    def check_tasks(self):
        for task in self.tasks:
            task()

    def update_stack(self):
        self.add_received_task()
        self.check_tasks()

    def update(self):
        self.update_stack()
        if self.stack:
            task = self.stack[-1]

            if isinstance(self.stack[-1], tuple):
                self.stack.pop(-1)

                task[0](task[1])

            else:
                is_continue = task() # only menus can return True
                if not is_continue:
                    self.stack.pop(-1)
                    display.clear()

    def run(self):
        while True:
            self.update()
