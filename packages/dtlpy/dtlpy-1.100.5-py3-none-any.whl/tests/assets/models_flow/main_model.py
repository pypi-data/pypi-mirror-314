import dtlpy as dl
import logging
import os
import random

logger = logging.getLogger('dummy-adapter')


@dl.Package.decorators.module(name='model-adapter',
                              description='Model Adapter for Dummy Model',
                              init_inputs={'model_entity': dl.Model, "test": "String"})
class ModelAdapter(dl.BaseModelAdapter):
    """
    Dummy Model adapter using pytorch.
    The class bind Dataloop model and model entities with model code implementation
    """

    def __init__(self, test, model_entity=None):
        super(ModelAdapter, self).__init__(model_entity=model_entity)
        self.test = test

    def load(self, local_path, **kwargs):
        logger.info("Loaded model")

    def save(self, local_path, **kwargs):
        logger.info("Saved model")

    def train(self, data_path, output_path, **kwargs):
        if self.test != 'default_value':
            raise ValueError(f"test is not set to default_value: {self.test}")
        logger.info("model training")
        print(self.model_entity.id)

    def predict(self, batch, **kwargs):
        logger.info("model prediction")
        batch_annotations = list()

        for img in batch:
            collection = dl.AnnotationCollection()
            for index in range(5):
                collection.add(
                    annotation_definition=dl.Box(label=self.model_entity.labels[index], top=index * 10, left=index * 10,
                                                 bottom=index * 10 + 10, right=index * 10 + 10),
                    model_info={'name': "test-model",
                                'confidence': 0.5,
                                'model_id': self.model_entity.id,
                                'dataset_id': self.model_entity.dataset_id})
                logger.debug("Predicted {} ({})".format(str(index), index * 0.1))
            batch_annotations.append(collection)

        return batch_annotations

    def convert_from_dtlpy(self, data_path, **kwargs):
        logger.info("convert_from_dtlpy")
