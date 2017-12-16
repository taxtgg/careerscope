from celery import Celery
from engine import celeryconfig

celery = Celery(__name__, broker=celeryconfig.CELERY_BROKER_URL)
celery.config_from_object('celeryconfig')
