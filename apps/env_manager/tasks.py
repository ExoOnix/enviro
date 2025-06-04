from core.celery import app

@app.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y
