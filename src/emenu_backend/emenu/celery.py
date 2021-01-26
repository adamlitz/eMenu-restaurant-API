import os
from celery import Celery

# Prevent 'django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emenu.settings")

from emails_backend.tasks import look_for_dish_updates

app = Celery("emenu")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    self.delay()
    print(f'Request: {self.request!r}')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    pass


@app.task
def test(arg):
    print(arg)
