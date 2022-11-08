import spacy

class Attention:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.deps = {}

    def process_message(self, msg):
        self.doc = self.nlp(msg)
        for tok in self.attention:
            self.dep[tok.head] += [tok.dep_]
    
    def get_attention_at(self, key):
        return self.deps[key]
