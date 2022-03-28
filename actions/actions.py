import random
from typing import Any, Text, Dict, List
from xmlrpc.client import boolean

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

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
        ActionQueryKnowledgeBase.filterFeatures = {}
        for header in self.data['apps'][0].keys():
            ActionQueryKnowledgeBase.filterFeatures[header] = set()
    
    #default name for action
    def name(self):
        return 'action_query_data_base'

    # amount of apps after filtering
    def getCurrentAppSize(self) -> int:
        return len(ActionQueryKnowledgeBase.currentApps)

    # search without filter --> override apps in action
    def searchInApps(self, header, value) -> None:
        ActionQueryKnowledgeBase.currentApps = []
        ActionQueryKnowledgeBase.filterFeatures[header].update(value)

        for x in self.data['apps']:
            if value in x[header]:
                ActionQueryKnowledgeBase.currentApps.append(x)
    
    # filter apps when already initialized
    def filterCurrentApps(self, header, value) -> None:
        filteredApps = []
        ActionQueryKnowledgeBase.filterFeatures[header].update(value)

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
        filter = super().getCurrentAppSize() != 0
        for obj in tracker.latest_message['entities']:
            if not (super().inHeaders(obj['entity'])): continue
            if filter:
                super().filterCurrentApps(obj['entity'], obj['value'])
            else:
                filter = True
                super().searchInApps(obj['entity'], obj['value'])

        dispatcher.utter_message(text=super().dispatchAppInfo())

# si tenim low confidence en algun cas, pero encara podem aplicar filtering, ho fem
class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="my_custom_fallback_template")
        found = False

        for obj in tracker.latest_message['entities']:
            if obj["entity"] == "mention":
                err = super().treatMention(obj["value"])
                if err != "": 
                    dispatcher.utter_message(text=err)
                    return None   
                found = True 
            else:
                if super().inHeaders(obj['entity']):
                    super().searchInApps(obj['entity'], obj['value'])
                found = True

        # Revert user message which led to fallback.
        if (found and super().getCurrentAppSize() == 0) or (not found):
            return [UserUtteranceReverted()]