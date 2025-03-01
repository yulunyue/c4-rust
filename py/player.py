# Framework: Standard Python

class Player:
    def __init__(self):
        self.message = ""
        self.drones = []
        self.scans = set()
        self.visible_fishes = set()
        self.count_fish_saved = []
        self.points = 0
        self.index = -1
        self.score = 0

    def get_expected_output_lines(self):
        return len(self.drones)

    def get_message(self):
        return self.message

    def get_index(self):
        return self.index

    def set_score(self, score):
        self.score = score

    def reset(self):
        self.message = ""
        for drone in self.drones:
            drone.move_command = None
            drone.fishes_scanned_this_turn = []
            drone.did_report = False
            drone.message = ""