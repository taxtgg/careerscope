import os

"""
Celery config:
http://docs.celeryproject.org/en/latest/configuration.html
"""


broker_url = os.environ.get('CELERY_BROKER_URL', 'amqp://localhost')
result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'rpc://localhost')
result_persistent = os.environ.get('CELERY_RESULT_PERSISTENT', True)
task_serializer = 'json'
result_serializer = 'json'
accept_content = os.environ.get('CELERY_ACCEPT_CONTENT', ['pickle', 'json', 'msgpack', 'yaml'])

include=['engine.tasks']

timezone = ('PROJECT_TIMEZONE', 'America/Los_Angeles')
enable_utc = True


"""
broker='amqp://',
backend='amqp://',
include=['engine.tasks']
"""