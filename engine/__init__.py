from __future__ import absolute_import, unicode_literals
from celery import Celery


celery = Celery('engine')
celery.config_from_object('engine.celeryconfig')


if __name__ == '__main__':
    celery.start()