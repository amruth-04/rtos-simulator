class Mutex:

    def __init__(self, name):

        self.name = name
        self.owner = None

    def acquire(self, task):

        # If nobody owns mutex
        if self.owner is None:

            self.owner = task

            return True

        # Mutex already locked
        return False

    def release(self):

        self.owner = None