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