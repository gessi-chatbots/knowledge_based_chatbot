import random
from typing import Any, Text, Dict, List
from xmlrpc.client import boolean

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

from actions.KnowledgeBase import KnowledgeBase

#reimplementation of ActionQueryKnowledgeBase
class ActionQueryKnowledgeBase(Action):
    #initiates data from knowledge base json file
    def __init__(self): 
        self.ordinal_mention_mapping = {
            "ANY": lambda l: random.choice(l),
            "LAST": lambda l: l[-1],
        }

        ActionQueryKnowledgeBase.currentApps = []
        ActionQueryKnowledgeBase.kb = KnowledgeBase()
    
    #default name for action
    def name(self):
        return 'action_query_data_base'

    # amount of apps after filtering
    def getCurrentAppSize(self) -> int:
        return len(ActionQueryKnowledgeBase.currentApps)

    # search without filter --> override apps in action
    def searchInApps(self, header, value) -> None:
        ActionQueryKnowledgeBase.currentApps = []
        ActionQueryKnowledgeBase.kb.updateFilterFeatures(header, value)

        data = ActionQueryKnowledgeBase.kb.getData()
        for x in data:
            if value in x[header]:
                ActionQueryKnowledgeBase.currentApps.append(x)
    
    # filter apps when already initialized
    def filterCurrentApps(self, header, value) -> None:
        filteredApps = []
        ActionQueryKnowledgeBase.kb.updateFilterFeatures(header, value)

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
        return header in ActionQueryKnowledgeBase.kb.getData()[0].keys()
    
    # if the mention isn't valid, invalidate search otherwise return correct app
    def treatMention(self, value) -> Text:
        if value.isnumeric():
            x = int(value)-1
            if x < 0 or x >= len(ActionQueryKnowledgeBase.currentApps):
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