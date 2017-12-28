import celery


app = celery.Celery('engine')
app.config_from_object('engine.celeryconfig')


if __name__ == '__main__':
    app.start()