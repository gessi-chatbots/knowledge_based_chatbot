import unittest
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from knowledge_based_chatbot.actions.actions import (
    RequestInformationEvent,
    findFeautre,
    ActionDefaultFallback,
)

class TestFindFeature(unittest.TestCase):
    def test_run(self):
        ff = findFeautre()
        dispatcher = CollectingDispatcher()
        tracker = Tracker(
            sender_id="",
            slots={},
            latest_message={
                "entities": [
                    {
                        "entity": "feature",
                        "value": "Calendar"
                    }
                ]
            },
            events=[],
            paused=False,
            active_loop={}
        )
        ff.run(dispatcher, tracker, {})
        self.assertEquals(dispatcher.messages["text"],  
                "Sure! I see you have multiple apps with this feature:\n1. Etar \n2. Simple Calendar \nDo you wish to use any app in particular?\n")

        tracker = Tracker(
            sender_id="",
            slots={},
            latest_message={
                "entities": [
                    {
                        "entity": "mention",
                        "value": "1"
                    }
                ]
            },
            events=[],
            paused=False,
            active_loop={}
        )
        ff.run(dispatcher, tracker, {})
        self.assertEquals(dispatcher.messages["text"],  
                "Great! Then let's launch Etar!\n")

class TestActionDefaultFallback(unittest.TestCase):
    def test_run(self):
        ff = ActionDefaultFallback()
        dispatcher = CollectingDispatcher()
        tracker = Tracker(
            sender_id="",
            slots={},
            latest_message={
                "entities": [
                    {
                        "entity": "feature",
                        "value": "Calendar"
                    }
                ]
            },
            events=[],
            paused=False,
            active_loop={}
        )
        ff.run(dispatcher, tracker, {})
        self.assertEquals(dispatcher.messages["text"],  
                "Sure! I see you have multiple apps with this feature:\n1. Etar \n2. Simple Calendar \nDo you wish to use any app in particular?\n")

        tracker = Tracker(
            sender_id="",
            slots={},
            latest_message={
                "entities": [
                    {
                        "entity": "mention",
                        "value": "1"
                    }
                ]
            },
            events=[],
            paused=False,
            active_loop={}
        )
        ff.run(dispatcher, tracker, {})
        self.assertEquals(dispatcher.messages["text"],  
                "Great! Then let's launch Etar!\n")

class TestCreateEvent(unittest.TestCase):
    def test_run(self):
        ff = findFeautre()
        dispatcher = CollectingDispatcher()
        tracker = Tracker()
        ff.run(dispatcher, tracker, {})
        self.assertEquals(dispatcher.messages["text"],  "Please provide the start date/time: ")

        #second run produces the same output
        ff.run(dispatcher, tracker, {})
        self.assertEquals(dispatcher.messages["text"],  "Please provide the start date/time: ")

class TestRequestInformationEvent(unittest.TestCase):
    def test_run(self):
        ri = RequestInformationEvent()
        ff = findFeautre()
        dispatcher = CollectingDispatcher()
        tracker = Tracker(
            sender_id="",
            slots={},
            latest_message={
                "entities": [
                    {
                        "entity": "information_date",
                        "value": "August 25th"
                    }
                ]
            },
            events=[],
            paused=False,
            active_loop={}
        )
        ff.run(dispatcher, tracker, {})
        self.assertEquals(dispatcher.messages["text"],  "Please provide the end date/time:")

        tracker = Tracker(
            sender_id="",
            slots={},
            latest_message={
                "entities": [
                    {
                        "entity": "information_date",
                        "value": "August 26th"
                    }
                ]
            },
            events=[],
            paused=False,
            active_loop={}
        )
        ff.run(dispatcher, tracker, {})
        self.assertEquals(dispatcher.messages["text"],  "Please provide the invites:")

        tracker = Tracker(
            sender_id="",
            slots={},
            latest_message={
                "entities": [
                    {
                        "entity": "information_email",
                        "value": "ccg.campas@gmail.com"
                    },
                    {
                        "entity": "information_text",
                        "value": "this is a name"
                    },
                    {
                        "entity": "information_email",
                        "value": "ccg.campas@gmail.com"
                    },
                ]
            },
            events=[],
            paused=False,
            active_loop={}
        )
        ff.run(dispatcher, tracker, {})
        self.assertEquals(dispatcher.messages["text"],  "Please provide the description:")