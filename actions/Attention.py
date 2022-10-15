import spacy


class Attention:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_trf")

    def process_message(self, msg):
        doc = self.nlp(msg)
        assert isinstance(doc._.custom_attr, TransformerData)
        print(doc._.custom_attr.tensors)
