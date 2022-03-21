from asyncore import dispatcher
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json 
class ActionQueryKnowledgeBase(Action):
    def __init__(self): 
        with open('rasa_knowledge_base.json', 'r') as f:
            self.data = json.load(f)
            ActionQueryKnowledgeBase.currentApps = []
    
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

class findFeautre(ActionQueryKnowledgeBase):
    def name(self):
        return 'action_find_feature'
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        obj = tracker.latest_message['entities'][0]
        super().searchInApps(obj['entity'], obj['value'])
        dispatcher.utter_message(text=super().dispatchAppInfo())
        
class filterFeature(ActionQueryKnowledgeBase):
    def name(self):
        return 'action_launch_app'
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        obj = tracker.latest_message['entities'][0]
        super().filterCurrentApps(obj['entity'], obj['value'])
        dispatcher.utter_message(text=super().dispatchAppInfo())