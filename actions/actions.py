import random
from typing import Any, Text, Dict, List
from xmlrpc.client import boolean

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json 
class ActionQueryKnowledgeBase(Action):
    def __init__(self): 
        with open('rasa_knowledge_base.json', 'r') as f:
            self.data = json.load(f)

            self.ordinal_mention_mapping = {
            "1": lambda l: l[0],
            "2": lambda l: l[1],
            "3": lambda l: l[2],
            "4": lambda l: l[3],
            "5": lambda l: l[4],
            "6": lambda l: l[5],
            "7": lambda l: l[6],
            "8": lambda l: l[7],
            "9": lambda l: l[8],
            "10": lambda l: l[9],
            "ANY": lambda l: random.choice(l),
            "LAST": lambda l: l[-1],
        }

            ActionQueryKnowledgeBase.currentApps = []
            self.possibleHeaders = self.data['apps'][0].keys()
    
    def name(self):
        return 'action_query_data_base'

    def searchInApps(self, header, value) -> None:
        ActionQueryKnowledgeBase.currentApps = []
        for x in self.data['apps']:
            if value in x[header]:
                ActionQueryKnowledgeBase.currentApps.append(x)
    
    def filterCurrentApps(self, header, value) -> None:
        filteredApps = []
        for x in self.currentApps:
            if value in x[header]:
                filteredApps.append(x)
        ActionQueryKnowledgeBase.currentApps = filteredApps

    def dispatchAppInfo(self) -> Text:
        size = len(ActionQueryKnowledgeBase.currentApps)
        text = ""
        if (size == 0): 
            text = "Sorry, I couldn't find any apps with those features!"
        elif (size == 1): 
            text = "Great! Then let's launch " + ActionQueryKnowledgeBase.currentApps[0]['name'] + "!\n"
        else: 
            text = "Sure! I see you have multiple apps with this feature:\n"
            i = 1
            for x in ActionQueryKnowledgeBase.currentApps:
                text += str(i) + ". " + x['name'] + " \n"
                i += 1
            text += "Do you wish to use any app in particular?\n"
        return text
    
    def inHeaders(self, header) -> boolean:
        return header in self.possibleHeaders
    
    def treatMention(self, value) -> None:
        if not (value in self.ordinal_mention_mapping.keys()):
            #change to error mapping
            ActionQueryKnowledgeBase.currentApps = []
        else:
           aux = self.ordinal_mention_mapping[value](ActionQueryKnowledgeBase.currentApps)
           ActionQueryKnowledgeBase.currentApps = [aux]

class findFeautre(ActionQueryKnowledgeBase):
    def name(self):
        return 'action_find_feature'
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        filter = False
        for obj in tracker.latest_message['entities']:
            if not (super().inHeaders(obj['entity'])): continue
            if filter:
                super().filterCurrentApps(obj['entity'], obj['value'])
            else:
                filter = True
                super().searchInApps(obj['entity'], obj['value'])

        dispatcher.utter_message(text=super().dispatchAppInfo())
        
class filterFeature(ActionQueryKnowledgeBase):
    def name(self):
        return 'action_launch_app'
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message['entities'])
        for obj in tracker.latest_message['entities']:
            if obj["entity"] == "mention":
                super().treatMention(obj["value"])
                continue
            if not (super().inHeaders(obj['entity'])): continue
            super().searchInApps(obj['entity'], obj['value'])
        dispatcher.utter_message(text=super().dispatchAppInfo())