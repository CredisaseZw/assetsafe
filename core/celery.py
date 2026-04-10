import logging
import os

from celery import Celery

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Standard auto-discovery: looks for tasks.py at the root of each installed app.
app.autodiscover_tasks()

# Additionally discover tasks nested under services/tasks.py, which is the
# convention used in this project's own apps.
app.autodiscover_tasks(
    [
        "apps.common",
        "apps.individuals",
        "apps.companies",
    ],
    related_name="services.tasks",
)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    logger.info("Request: %r", self.request)
