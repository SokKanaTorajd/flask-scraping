from celery import Celery
from app.models import config

worker = Celery(__name__)
worker.conf.broker_url = config.MONGODB_URI
worker.conf.result_backend = config.MONGODB_URI
worker.conf.mongodb_backend_settings = {
        'database': 'system_log',
        'taskmeta_collection': 'task_log'
    }
