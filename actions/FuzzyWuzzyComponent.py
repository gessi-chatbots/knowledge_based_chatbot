'''
from typing import Dict, Text, Any, List, Optional

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.extractors.extractor import EntityExtractor

import json
import os
@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR], is_trainable=True
)
class FuzzyWuzzyComponent(EntityExtractor, GraphComponent):
    def __init__(
        self,
        model_storage: ModelStorage,
        resource: Resource,
        training_artifact: Optional[Dict],
    ) -> None:
        # Store both `model_storage` and `resource` as object attributes to be able
        # to utilize them at the end of the training
        self._model_storage = model_storage
        self._resource = resource

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(model_storage, resource, training_artifact=None)

    @classmethod
    def load(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
        **kwargs: Any,
    ) -> FuzzyWuzzyComponent:
        try:
            with model_storage.read_from(resource) as directory_path:
                with open(directory_path / "artifact.json", "r") as file:
                    training_artifact = json.load(file)
                    return cls(
                        model_storage, resource, training_artifact=training_artifact
                    )
        except ValueError:
            print("no persisted data for your component")


    def train(self, training_data: TrainingData) -> Resource:
        # TODO: Implement this if your component requires training
        
        # Persist your graph component
        with self._model_storage.write_to(self._resource) as directory_path:
            with open(directory_path / "artifact.json", "w") as file:
                json.dump({"my": "training artifact"}, file)

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        # TODO: Implement this if your component augments the training data with
        #       tokens or message features which are used by other components
        #       during training.

        return training_data

    def process(self, messages: List[Message]) -> List[Message]:
        return messages
    
    def process(self, message: Message, **kwargs: Any) -> None:
        metadata = message.get("metadata")
        print(metadata.get("intent"))
        print(metadata.get("example"))

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        if self.entities:
            file_name = file_name + ".json"
            entity_file = os.path.join(model_dir, file_name)
            write_json_to_file(entity_file, self.entities)

            return {"file": file_name}
        else:
            return {"file": None}

        # n-grams
        # look for library
'''