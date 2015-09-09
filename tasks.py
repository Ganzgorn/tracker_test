from celery import Celery
from celery.signals import task_postrun
import requests
from requests.auth import HTTPBasicAuth

app = Celery('tasks', backend='redis', broker='redis://localhost:6379/0')


@app.task
def req_search_for_track_id(url, data, header, auth=None):
    """
    Выполняет запрос к ТК
    """
    http_auth = HTTPBasicAuth(auth[0], auth[1]) if auth else None
    response = requests.get(url, data=data, headers=header, auth=http_auth)
    return response.text


@task_postrun.connect
def task_postrun_handler(sender, task_id, **kwargs):
    """
    Результат выполнения передаем сервису
    """
    url = 'http://localhost:5000/result_celery/'
    data = {
        'task_id': task_id,
        'message': kwargs.get('retval')
    }
    requests.post(url, data)