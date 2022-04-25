import random
from typing import Any, Text, Dict, List
from xmlrpc.client import boolean

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

import json 

class KnowledgeBase():
    def __init__(self):
        with open('rasa_knowledge_base.json', 'r') as f:
            self.data = json.load(f)

        KnowledgeBase.features = {}
        KnowledgeBase.filterFeatures = {}
        for header in self.data['apps'][0].keys():
            KnowledgeBase.features[header] = set()
            KnowledgeBase.filterFeatures[header] = set()
    
    def getFilterFeatures(self) -> Dict:
        return KnowledgeBase.filterFeatures
    
    def setFilterFeatures(self, ff) -> None:
        KnowledgeBase.filterFeatures = ff
    
    def updateFilterFeatures(self, header, value) -> None:
        KnowledgeBase.filterFeatures[header].update(value)

    def getFeatures(self) -> Dict:
        return self.features