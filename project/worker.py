import os
from celery import Celery
from model import IrisModel
import sklearn

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

model = IrisModel()

@celery.task(name='create_task')
def create_task(sepal_length, sepal_width, petal_length, petal_width):
    #model = IrisModel()
    prediction, probability= model.predict_species(sepal_length, sepal_width, petal_length, petal_width)
    return {
        'prediction': prediction,
        'probability': probability
    }