from common.communication import RadioClient

class Micro_Bit_Client:

    message_types = {}
    tasks = []
    stack_indexes = []

    def __init__(self):
        self.stack = []
        self.radio_client = RadioClient()

    def add_received_task(self):
        message_type, message_data = self.radio_client.get_message()

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
        if message_type in self.stack_indexes:
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
