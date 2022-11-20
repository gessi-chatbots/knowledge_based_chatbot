import spacy

class Attention:
    def __init__(self, msg):
        self.nlp = spacy.load('en_core_web_sm')
        self.deps = {}
        self.process_message(msg)

    def process_message(self, msg):
        self.doc = self.nlp(msg)
        for tok in self.doc:
            if tok.head not in self.deps: self.deps[tok.head] = []
            self.deps[tok.head] += [tok.dep_]
    
    def get_attention_at(self, key):
        ret = {}

        for k in key:
            if k in self.deps.keys():
                ret[k] = self.deps[k]

        return ret