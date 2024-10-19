import time

class Goal:
    def __init__(self):
        self.text = None
        self.remind_delay = None
        self.created = time.time()
        self.notification = None
        self.alive = True
        self.prompt()

    def prompt(self):
        # Pass default time load
        pass

    def follow_up(self):
        pass

    def trigger(self):
        pass


    def is_alive(self):
        return self.alive