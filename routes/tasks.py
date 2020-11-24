from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from drivehome import celery_app
from .models import Route

logger = get_task_logger(__name__)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0),
        measure_routes,
    )


@celery_app.task
def measure_routes():
    logger.info("Measuring started")
    for route in Route.objects.all():
        logger.info(str(route))
        route.measure()
    logger.info("Measuring completed")
