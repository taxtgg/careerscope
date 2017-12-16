import os


"""
Celery config:
http://docs.celeryproject.org/en/latest/configuration.html
"""


broker_url = os.environ.get('CELERY_BROKER_URL', 'amqp://localhost')
result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'amqp://localhost')
task_serializer = 'json'
result_serializer = 'json'
accept_content = os.environ.get('CELERY_ACCEPT_CONTENT', ['pickle', 'json', 'msgpack', 'yaml'])
timezone = ('PROJECT_TIMEZONE', 'America/Los_Angeles')
enable_utc = True

