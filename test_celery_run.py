from celery import Celery

app = Celery('test', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task
def add(x, y):
    return x + y

if __name__ == '__main__':
    r = add.delay(2, 3)
    print("Sent:", r.id)
