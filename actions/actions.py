import random
from typing import Any, Dict, List, Text
from xmlrpc.client import boolean

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.ActionQueryKnowledgeBase import ActionQueryKnowledgeBase
from actions.EventHandler import EventHandler

eh = EventHandler()
class findFeautre(ActionQueryKnowledgeBase):
    def name(self):
        return "action_find_feature"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        filter = super().getCurrentAppSize() != 0
        print(tracker.latest_message["entities"])
        for obj in tracker.latest_message["entities"]:
            if obj["entity"] == "mention":
                ret = super().treatMention(obj["value"])
                if ret != "":
                    dispatcher.utter_message(ret)
                break

            if not (super().inHeaders(obj["entity"])):
                continue
            if filter:
                super().filterCurrentApps(obj["entity"], obj["value"])
            else:
                filter = True
                super().searchInApps(obj["entity"], obj["value"])

        dispatcher.utter_message(text=super().dispatchAppInfo())


# si tenim low confidence en algun cas, pero encara podem aplicar filtering, ho fem
class ActionDefaultFallback(ActionQueryKnowledgeBase):
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

        for obj in tracker.latest_message["entities"]:
            if obj["entity"] == "mention":
                err = super().treatMention(obj["value"])
                if err != "":
                    dispatcher.utter_message(text=err)
                    return None
                found = True
            else:
                if super().inHeaders(obj["entity"]):
                    super().searchInApps(obj["entity"], obj["value"])
                found = True

        # Revert user message which led to fallback.
        if (found and super().getCurrentAppSize() == 0) or (not found):
            return [UserUtteranceReverted()]

class CreateEvent(Action):
    def name(self):
        return "action_create_event"
    
    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        print(tracker.latest_message)
        eh.reset()
        msg = eh.get_initial_message() + f"""Please provide the '{eh.get_next_slot()}': """
        
        dispatcher.utter_message(text=msg)
        return []

class RequestInformationEvent(Action):
    def name(self):
        return "action_request_information"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        if eh.get_current_key_value() > -1:
            for obj in tracker.latest_message["entities"]:
                count = eh.count_properties(obj["entity"].replace("information_", ""))
                if count > 0:
                    #TODO: contextualize the information
                    if obj["entity"] == "information_email":
                        eh.set_information(obj["value"])
                    elif obj["entity"] == "information_text":
                        eh.set_information(obj["value"])
                    elif obj["entity"] == "information_calendar":
                        eh.set_information(obj["value"])
        if eh.hasNextSlot():
            msg = (
                f"""Please provide the '{eh.get_next_slot()}': """
            )
            dispatcher.utter_message(text=msg)
        elif eh.atEnd():
            dispatcher.utter_message(
                text="Thank you for your information!\n"
                + "Please confirm the following is correct:\n"
                + eh.dispatchEventInfo()
            )
            eh.reset()

        return []


class ValidateEvent(Action):
    def name(self):
        return "action_validate_event"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        eh.write_to_file()
