import random
from typing import Any, Text, Dict, List, Set
from xmlrpc.client import boolean

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

import json 

class KnowledgeBase():
    def __init__(self):
        with open('rasa_knowledge_base.json', 'r') as f:
            self.data = json.load(f)
        self.features = set()
        self.filterFeatures = {}
        
        for header in self.data['apps'][0].keys():
            self.filterFeatures[header] = set()

        for app in self.data['apps']:
            self.features.update(app['features'])
    
    def getFilterFeatures(self) -> Dict:
        return self.filterFeatures
    
    def setFilterFeatures(self, ff) -> None:
        self.filterFeatures = ff
    
    def updateFilterFeatures(self, header, value) -> None:
        self.filterFeatures[header].update(value)

    def getFeatures(self) -> Set:
        return self.features
    
    def getData(self) -> Dict:
        return self.data['apps']