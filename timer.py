import time


class Typing_Timer:
    def __init__(self):
        self.counter = 0
        self.started = False
        self.start_time = 0.0
        self.end_time = 0.0
        self.text = ''

    def start(self, text):
        self.counter = 0
        self.started = True
        self.start_time = time.time()
        self.end_time = 0.0
        self.text = text

    def end(self):
        self.started = False
        self.end_time = time.time()

    def increase_counter(self):
        self.counter += 1
