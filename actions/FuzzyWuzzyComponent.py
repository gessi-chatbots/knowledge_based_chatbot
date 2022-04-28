import typing
from typing import Dict, Text, Any, List, Optional

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.extractors.extractor import EntityExtractorMixin
from rasa.shared.nlu.constants import ENTITIES

import fuzzywuzzy

from actions.KnowledgeBase import KnowledgeBase

# TODO: Correctly register your component with its type
@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR], is_trainable=False
)
class FuzzyWuzzyComponent(GraphComponent, EntityExtractorMixin):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        kb = KnowledgeBase()
        super().__init__(component_config)
        self.score_cutoff = component_config.get(
            "score_cutoff", self.defaults["score_cutoff"]
        )
    
    defaults = {"score_cutoff": 80}

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config)

    @staticmethod
    def required_packages() -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return ["fuzzywuzzy"]

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        """Processes the training examples in the given training data in-place."""
        self.process(training_data.training_examples)
        return training_data

    def process(self, messages: List[Message]) -> List[Message]:
        """Processes incoming message and compute and set features."""
        for message in messages:
            entities = message.get(ENTITIES, [])
            message.set(ENTITIES, self._fix_typo(entities), add_to_output=True)
        return messages

    def _fix_typo(self, entities: List[Dict[Text, Any]]) -> List[Dict[Text, Any]]:
        entities_fixed = []
        for entity in entities:
            if entity['entity'] != 'features': continue
            value = str(entity["value"])
            match = fuzzywuzzy.process.extractOne(
                value, self.kb.getFeatures(), score_cutoff=self.score_cutoff
            )
            if match:
                entity["value"] = match[0]

            entities_fixed.append(entity)
        
        return entities_fixed