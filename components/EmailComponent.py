import re
from typing import Any, Dict, List, Optional, Text

from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.extractors.extractor import EntityExtractorMixin
from rasa.shared.nlu.constants import ENTITIES, TEXT
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData


@DefaultV1Recipe.register([DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR], is_trainable=True)
class EmailComponent(GraphComponent, EntityExtractorMixin):
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        self._config = component_config

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
        return ["re"]

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        """Processes the training examples in the given training data in-place."""
        self.process(training_data.training_examples)
        return training_data

    def process(self, messages: List[Message]) -> List[Message]:
        """Processes incoming message and compute and set features."""
        for message in messages:
            emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', message.get(TEXT))
            entities = message.get(ENTITIES, [])
            message.set(ENTITIES, self._check_found_emails(entities, emails), add_to_output=True)
        return messages

    def _check_found_emails(self, entities: List[Dict[Text, Any]], emails: List[Text]) -> List[Dict[Text, Any]]:
        entities_fixed = entities

        for entity in entities:
            if entity["entity"] == "information_email":
                if entity["value"] in emails:
                    emails.remove(entity["value"])
        
        for email in emails:
            entities_fixed.append({"entity": "information_email",
                                    "value": email,
                                    "extractor": "EmailComponent"
                            })

        return entities_fixed

    def train(self, training_data: TrainingData) -> Resource:
        # TODO: Implement this if your component requires training
        pass
