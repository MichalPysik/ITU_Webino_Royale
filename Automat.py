
class automat_class:
    def __init__(self):
        self.Slot1 = "/static/SKINS/7.png"
        self.Slot2 = "/static/SKINS/7.png"
        self.Slot3 = "/static/SKINS/7.png"
        self.Slots = [7,7,7]
        return

    def set_slots(self, Slots):
        try:
            self.Slot1 = "/static/SKINS/" + str(Slots[0]) + ".png"
            self.Slot2 = "/static/SKINS/" + str(Slots[1]) + ".png"
            self.Slot3 = "/static/SKINS/" + str(Slots[2]) + ".png"
            self.Slots = Slots
        except:
            return 1
        return 0

    def get_slots(self):
        return self.Slots

    def slots_for_HTML(self):
        return [self.Slot1, self.Slot2, self.Slot3]