import os

class UrandomReader():
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        pass
    def next_bytes(self, count):
        return os.urandom(count)

class RandomReader():
    def __init__(self):
        self.file = None
    def __enter__(self):
        if os.stat("/dev/random"):
            self.file = open("/dev/random", "rb")
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
    def next_bytes(self, count):
        if self.file is None:
            return os.urandom(count)
        else:
            return self.file.read(count)
