import json

from dateutil import parser


class EventHandler:
    def __init__(self):
        self.file = "init-payload.json"
        self.get_info()
        self.key = -1

    def get_info(self):
        with open(self.file, "r") as f:
            self.text = json.load(f)
        self.dict = self.text["target_data"]

        self.type = set()
        self.type_set_of = set()
        self.amount_type = {}
        for d in self.dict:
            t = d["type"]
            if t not in self.amount_type.keys(): self.amount_type[t] = 0
            self.amount_type[t] += 1
            
            if "SefOf" in t:
                self.type_set_of.update([t.split("::")[1]])
            else:
                self.type.update(t)
    
    def set_text(self, text):
        self.text = text["initial_data"]
        self.dict = self.text["target_data"]

    def get_initial_message(self):
        s = "Let's get started! The following information is required: \n"
        for x in self.dict:
            s += "  - " + x["name"] + "\n"
        
        s += '\n'
        return s

    def get_current_key_value(self):
        return self.key
    
    def get_next_slot(self):
        self.aug_key()
        print(self.dict[self.key])
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
    
    def set_information(self, value, attention):
        d = self.dict[self.key]
        for d in self.dict:
            if d["type"] in attention:
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
        self.key = -1
        self.get_info()
    
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
