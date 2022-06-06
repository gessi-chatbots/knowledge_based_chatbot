import json

from dateutil import parser


class EventHandler:
    def __init__(self):
        file = "init-payload.json"
        with open(file, "r") as f:
            self.text = json.load(f)
        self.dict = self.text["target_data"]
        print(self.dict)
        self.key = -1

    def get_current_key_value(self):
        return self.key
    
    def get_next_slot(self):
        self.aug_key()
        return self.dict[self.key]["name"]

    def aug_key(self):
        self.key += 1

    def set_information(self, value):
        d = self.dict[self.key]
        if d["value"] is None:
            if "SetOf" in d["type"]:
                d["value"] = [value]
            else:
                d["value"] = value
        else:
            if not("SetOf" in d["type"]):
                v = d["value"] + " " + value

                if d["type"] == "Calendar":
                    v = str(parser.parse(v))

                d["value"] = v
            else:
                d["value"].append(value)
        
        self.dict[self.key] = d
        print(d)

    def hasNextSlot(self):
        return self.key < len(self.dict) - 1

    def atEnd(self):
        return self.key == len(self.dict) - 1

    def dispatchEventInfo(self):
        t = ""
        for key in self.dict:
            print(key)
            print(key["name"])
            print(key["value"])
            t += "  -" + key["name"] + ": " + str(key["value"]) + "\n"
        return t

    def reset(self):
        self.dict = {}
        self.slots = []
        self.key = 0
    
    def write_to_file(self):
        file = "end-payload.json"
        with open(file, "w") as f:
            json.dump(self.text, f)

    def count_properties(self, type):
        count = 1
        for s in self.text["target_data"]:
            if s["type"] == type:
                count += 1
            
        return count
