from argparse import Action
from socket import AF_KEY
import unittest

from knowledge_based_chatbot.actions.ActionQueryKnowledgeBase import ActionQueryKnowledgeBase

class TestActionQueryKnowledgeBase(unittest.Test):
    def test_getCurrentAppSize(self):
        ak = ActionQueryKnowledgeBase()
        self.assertEquals(ak.getCurrentAppSize(), 0)

        ak.filterCurrentApps("feature", "Works Offline")
        self.assertEquals(ak.getCurrentAppSize(), 2)

        ak.filterCurrentApps("feature", "Works Offline")
        self.assertEquals(ak.getCurrentAppSize(), 2)

        ak.filterCurrentApps("feature", "GPS Navigation")
        self.assertEquals(ak.getCurrentAppSize(), 2)

        ak.filterCurrentApps("mention", "first")
        self.assertEquals(ak.getCurrentAppSize(), 1)

        ak.filterCurrentApps("feature", "Works Offline")
        self.assertEquals(ak.getCurrentAppSize(), 2)

    def test_searchInApps(self, header, value):
        ak = ActionQueryKnowledgeBase()
        ak.filterCurrentApps("feature", "Works Offline")
        apps = ["OsmAnd", "Organic Maps"]
        self.assertEquals(ak.getCurrentApp() == apps)

        ak = ActionQueryKnowledgeBase()
        ak.filterCurrentApps("feature", "Calendar")
        apps = ["Etar", "Simple Calendar"]
        self.assertEquals(ak.getCurrentApp() == apps)

        ak = ActionQueryKnowledgeBase()
        ak.filterCurrentApps("feature", "NA")
        apps = []
        self.assertEquals(ak.getCurrentApp() == apps)

    def test_filterCurrentApps(self, header, value):
        ak = ActionQueryKnowledgeBase()
        ak.filterCurrentApps("feature", "Works Offline")
        apps = ["OsmAnd", "Organic Maps"]
        self.assertEquals(ak.getCurrentApp() == apps)

        ak.filterCurrentApps("feature", "Calendar")
        apps = []
        self.assertEquals(ak.getCurrentApp() == apps)

        ak.filterCurrentApps("feature", "Calendar")
        apps = ["Etar", "Simple Calendar"]
        self.assertEquals(ak.getCurrentApp() == apps)

    def dispatchAppInfo(self):
        ak = ActionQueryKnowledgeBase()
        ak.setCurrentApps([])
        self.assertEquals(ak.dispatchAppInfo(), "Sorry, I couldn't find any apps with those features!")

        ak.setCurrentApps(["App1"])
        self.assertEquals(ak.dispatchAppInfo(), "Great! Then let's launch App1!\n")

        ak.setCurrentApps(["App1", "App2"])
        self.assertEquals(ak.dispatchAppInfo(),  
                "Sure! I see you have multiple apps with this feature:\n1. App1 \n2. App2 \nDo you wish to use any app in particular?\n")
        
    def test_inHeaders(self):
        ak = ActionQueryKnowledgeBase()
        self.assertEquals(ak.inHeaders("id"), True)
        self.assertEquals(ak.inHeaders("name"), True)
        self.assertEquals(ak.inHeaders("features"), True)
        self.assertEquals(ak.inHeaders("na"), False)
        self.assertEquals(ak.inHeaders(""), False)


    def test_treatMention(self, value):
        ak = ActionQueryKnowledgeBase()
        self.assertEquals(ak.treatMention("0"), True)
        self.assertEquals(ak.treatMention("1"), True)
        self.assertEquals(ak.treatMention("2"), True)
        self.assertEquals(ak.treatMention("3"), True)
        self.assertEquals(ak.treatMention("-1"), False)
        self.assertEquals(ak.treatMention("10"), False)
        self.assertEquals(ak.treatMention("10000"), False)