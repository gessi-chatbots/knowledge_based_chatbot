import random
from typing import Any, Text, Dict, List
from xmlrpc.client import boolean

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json 
#reimplementation of ActionQueryKnowledgeBase
class ActionQueryKnowledgeBase(Action):
    #initiates data from knowledge base json file
    def __init__(self): 
        with open('rasa_knowledge_base.json', 'r') as f:
            self.data = json.load(f)

        self.ordinal_mention_mapping = {
            "ANY": lambda l: random.choice(l),
            "LAST": lambda l: l[-1],
        }

        ActionQueryKnowledgeBase.currentApps = []
    
    #default name for action
    def name(self):
        return 'action_query_data_base'

    # search without filter --> override apps in action
    def searchInApps(self, header, value) -> None:
        ActionQueryKnowledgeBase.currentApps = []
        for x in self.data['apps']:
            if value in x[header]:
                ActionQueryKnowledgeBase.currentApps.append(x)
    
    # filter apps when already initialized
    def filterCurrentApps(self, header, value) -> None:
        filteredApps = []
        for x in self.currentApps:
            if value in x[header]:
                filteredApps.append(x)
        ActionQueryKnowledgeBase.currentApps = filteredApps

    # structure message to utter
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
    
    # check if an item is in the headers i.e. can be filtered by
    def inHeaders(self, header) -> boolean:
        return header in self.data['apps'][0].keys()
    
    # if the mention isn't valid, invalidate search otherwise return correct app
    def treatMention(self, value) -> Text:
        if value.isnumeric():
            x = int(value)-1
            print(len(ActionQueryKnowledgeBase.currentApps))
            if x < 0 or x >= len(ActionQueryKnowledgeBase.currentApps):
                print("here")
                aux = []
                return "Incorrect value for given choices."
            aux = [ActionQueryKnowledgeBase.currentApps[x]]
        elif value in self.ordinal_mention_mapping:
            aux = [self.ordinal_mention_mapping[value](ActionQueryKnowledgeBase.currentApps)]
        else:
            aux = []
            return "Incorrect value for given choices."

        ActionQueryKnowledgeBase.currentApps = aux
        return ""


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
        for obj in tracker.latest_message['entities']:
            if obj["entity"] == "mention":
                err = super().treatMention(obj["value"])
                if err != "": 
                    dispatcher.utter_message(text=err)
                    return None    
            else:
                if super().inHeaders(obj['entity']):
                    super().searchInApps(obj['entity'], obj['value'])
                else: 
                    dispatcher.utter_message(text="No available filters.")
                    return None
            
            dispatcher.utter_message(text=super().dispatchAppInfo())