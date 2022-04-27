import random
from typing import Any, Text, Dict, List
from xmlrpc.client import boolean

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

import json 
from actions.ActionQueryKnowledgeBase import ActionQueryKnowledgeBase

class findFeautre(ActionQueryKnowledgeBase):
    def name(self):
        return 'action_find_feature'
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        filter = super().getCurrentAppSize() != 0
        print (tracker.latest_message['entities'])
        for obj in tracker.latest_message['entities']:
            if obj['entity'] == "mention": 
                ret = super().treatMention(obj['value'])
                if ret != "": dispatcher.utter_message(ret)
                break

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