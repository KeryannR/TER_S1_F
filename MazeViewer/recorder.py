import json

class Recorder:
    def __init__(self, filename="record.json"):
        self.filename = filename
        self.frames = []  # simplement ["u", "d", "l", "r", ...]

    def record_frame(self, letter):
        self.frames.append(letter)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.frames, f)

    def load(self):
        with open(self.filename, "r") as f:
            self.frames = json.load(f)

    @staticmethod
    def dir_to_letter(dx, dy):
        if (dx, dy) == (0, -1): return 'u'
        if (dx, dy) == (0, 1): return 'd'
        if (dx, dy) == (-1, 0): return 'l'
        if (dx, dy) == (1, 0): return 'r'
        return 's'

    @staticmethod
    def letter_to_dir(letter):
        return {'u': (0, -1), 'd': (0, 1), 'l': (-1, 0), 'r': (1, 0), 's': (0, 0)}.get(letter, (0,0))
