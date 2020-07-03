"""
Tasks to run in parallell
"""
from project.celery import app
from .services import process_namespaces_notifications


@app.task(bind=True,
          rate_limit='10/m',  # Max. 10 tasks per minute
          default_retry_delay=2 * 60,  # retry in 2m
          ignore_result=True)
def process_notifications(self):
    try:
        process_namespaces_notifications()
    except Exception as exc:
        raise self.retry(exc=exc)
