import typing
from typing import Any, Dict, List, Optional, Text

from fuzzywuzzy import process
from KnowledgeBase import KnowledgeBase
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.extractors.extractor import EntityExtractorMixin
from rasa.shared.nlu.constants import ENTITIES
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData


# TODO: Correctly register your component with its type
@DefaultV1Recipe.register([DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR], is_trainable=True)
class FuzzyWuzzyComponent(GraphComponent, EntityExtractorMixin):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        self._config = component_config
        self.kb = KnowledgeBase()

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        """Creates a new component (see parent class for full docstring)."""
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
        fts = list(self.kb.getFeatures())

        for entity in entities:
            if entity["entity"] == "features":
                value = str(entity["value"])
                match = process.extract(query=value, choices=fts, limit=1)
                if match:
                    entity["value"] = match[0][0]

            entities_fixed.append(entity)

        print(entities_fixed)
        return entities_fixed

    def train(self, training_data: TrainingData) -> Resource:
        # TODO: Implement this if your component requires training
        pass
