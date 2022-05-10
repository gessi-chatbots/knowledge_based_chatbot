import unittest
from KnowledgeBase import KnowledgeBase

class TestKnowledgeBase(unittest.TestCase):
    def test_SetFilterFeatures(self):
        kb = KnowledgeBase()
        ff = {
            'id': set(),
            'name': set({'app_name'}),
            'features': set({'feature1', 'feature2'}),
        }

        kb.setFilterFeatures(ff)
        self.assertEqual(kb.getFilterFeatures(), ff)

    def test_UpdateFilterFeatures(self):
        kb = KnowledgeBase()
        ff = {
            'id': set(),
            'name': set({'app_name'}),
            'features': set({'feature1', 'feature2'}),
        }
        for header in ff:
            for value in ff[header]:
                kb.updateFilterFeatures(header, [value])
        self.assertEqual(kb.getFilterFeatures(), ff)

class TestActionQueryKnowledgeBase(unittest.TestCase):
    def test_searchInApps(self):
        print ("hello world")
    
    def test_filterCurrentApps(self):
        print("hello world")

    def test_inHeaders(self):
        print("hello world")
    
    def test_treatMention(self):
        print("hello world")


class TestFindFeature (unittest.TestCase):
    def test_run(self):
        print("hello world")

class TestActionDefaultFallback(unittest.TestCase):
    def test_run(self):
        print("hello world")

if __name__ == '__main__':
    unittest.main()