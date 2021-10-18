from celery.app import task
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model import Species

from worker import create_task
from celery.result import AsyncResult

app = FastAPI(title='Flower Predictor')

@app.get('/')
def home():
    return {
        'message': 'Welcome to Flower Predictor!'
    }

@app.post('/predict', status_code=201)
def predict_species(payload: Species):
    payload = payload.dict()
    task = create_task.delay(
        payload['sepal_length'],
        payload['sepal_width'],
        payload['petal_length'],
        payload['petal_width']
    )
    return JSONResponse({'task_id': task.id})

@app.get('/predict/{task_id}')
def get_prediction(task_id):
    task_result = AsyncResult(task_id)
    result = {
        'task_id': task_id,
        'task_status': task_result.status,
        'task_result': task_result.result
    }
    return JSONResponse(result)
