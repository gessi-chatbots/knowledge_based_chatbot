import json


class EventHandler:
    def __init__(self, event):
        file = "form_info.json"
        with open(file, "r") as f:
            self.text = json.load(f)
        self.dict = dict.fromkeys(self.extract_slots(event))
        self.slots = list(self.dict.keys())
        self.nextKey = -1

    def extract_slots(self, event):
        return self.text[event]

    def get_next_slot(self):
        self.nextKey += 1
        return self.slots[self.nextKey]

    def get_current_slot(self):
        return self.slots[self.nextKey]

    def get_current_key_value(self):
        return self.nextKey

    def set_information(self, value):
        self.dict[self.get_current_slot()] = value
        print(self.dict)

    def hasNextSlot(self):
        return self.nextKey < len(self.slots) - 1

    def atEnd(self):
        return self.nextKey == len(self.slots) - 1

    def dispatchEventInfo(self):
        t = ""
        for key in self.dict:
            t += "  -" + key + ": " + self.dict[key] + "\n"
        return t

    def reset(self):
        self.dict = {}
        self.slots = []
        self.nextKey = -1
