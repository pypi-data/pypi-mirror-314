import importlib
from collections.abc import Callable
from datetime import date, datetime, time
from json import loads
from typing import Any, Iterator, Optional

from celery import chord, group, shared_task
from celery.canvas import Signature, signature
from croniter import croniter, croniter_range
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask, cronexp


class SynchronizationTask(PeriodicTask):
    RELATIVE_TASK_MODULE_PATH = "wbportfolio.models.synchronization.synchronization.task"

    dependent_task = models.ForeignKey(
        "self", related_name="dependency_tasks", null=True, blank=True, on_delete=models.SET_NULL
    )
    import_path = models.CharField(max_length=512, verbose_name="Import Path", default="", blank=True)

    @property
    def cast_args(self) -> list[Any]:
        """
        transform the string args representation into list. We except this to become unnecessary when django beat move to jsonfield
        :return: list
        """
        return loads(self.args or "[]")

    @property
    def cast_kwargs(self) -> dict[Any, Any]:
        """
        transform the string kwargs representation into dictionary. We except this to become unnecessary when django beat move to jsonfield
        :return: list
        """
        return loads(self.kwargs or "{}")

    @property
    def _import_method(self) -> Callable[[Any], Any]:
        """
        If a custom task is specified, return the loaded module as callabck. Otherwise, returns the default synchronization
        function defined in `_default_callback
        :return: Callable
        """
        if import_path := self.import_path:
            synchronize_module = importlib.import_module(import_path)
            return synchronize_module.callback
        else:
            return self._default_callback

    def schedule_str(self, filter_daily: Optional[bool] = False) -> str:
        """
        Returns the crontab string representation. If fitler_daily is true, we cast the crontab so that the lowest frequency
        becomes daily.
        :param filter_daily: bool (optional)
        :return: crontab string representation
        """
        crontab_minute = cronexp(self.crontab.minute)
        crontab_hour = cronexp(self.crontab.hour)
        if filter_daily:
            if crontab_minute == "*":
                crontab_minute = "0"
            if crontab_hour == "*":
                crontab_hour = "0"
        return "{0} {1} {2} {3} {4}".format(
            crontab_minute,
            crontab_hour,
            cronexp(self.crontab.day_of_month),
            cronexp(self.crontab.month_of_year),
            cronexp(self.crontab.day_of_week),
        )

    def dates_range(self, from_date: date, to_date: date, filter_daily: Optional[bool] = False) -> Iterator[datetime]:
        """
        returns a list of valid dates given an interval and a specific crontab schedule.
        :param from_date: date
        :param to_date: date
        :param filter_daily: bool (optional)
        :return: list[date]
        """
        min_datetime = datetime.combine(from_date, time.min)
        max_datetime = datetime.combine(to_date, time.max)
        return croniter_range(min_datetime, max_datetime, self.schedule_str(filter_daily=filter_daily))

    def is_valid_date(self, sync_datetime: datetime) -> bool:
        """
        check wether a date is valid given the stored crontab schedule
        :param sync_datetime: datetime
        :return: bool
        """
        return croniter.match(self.schedule_str(), sync_datetime)

    def save(self, *args: Any, **kwargs: Any):
        self.task = self.RELATIVE_TASK_MODULE_PATH
        if not self.schedule:
            self.crontab, _ = CrontabSchedule.objects.get_or_create(
                minute="0",
                hour="*",
                day_of_week="*",
                day_of_month="*",
                month_of_year="*",
            )
        if not self.crontab:
            raise ValueError("Synchronization task supports only Crontab Schedule")
        if self.crontab.minute == "*":
            raise ValueError("The minimum crontab frequency supported is hourly.")
        super().save(*args, **kwargs)

    def _tasks_signature(self, *args, **kwargs: Any) -> Signature:
        """
        Gather all tasks that needs to run under this synchronization job as a list of celery signatures.
        This method is expected to be implemented at each inheriting class.
        :param args: list
        :param kwargs: dict
        :return: list[signature]
        """
        raise NotImplementedError()

    def _default_callback(self, *args: Any, **kwargs: Any) -> Any:
        """
        The default synchronization function executed if no custom task is provided for this synchronization object.
        This method is expected to be implemented at each inheriting class.
        :param args: list
        :param kwargs: dict
        :return: callable
        """
        raise NotImplementedError()

    def _get_kwargs(self) -> Any:
        """
        return the base keyword argument to be injected into the `_tasks_signature` method. Define as a standalone function
        in order to allow subclass definition.
        :return: dict
        """
        return {"task_execution_datetime": timezone.now()}

    def _end_task_signature(self, **kwargs: Any) -> Signature:
        """
        A synchronization object can defined a dependant task that will be executed at this end of all returned task from
        _tasks_signatures.
        This function returns the signature of this chained task.
        :param kwargs:
        :return: signature
        """
        if self.dependent_task:
            kwargs = {"override_execution_datetime_validity": True, **self.dependent_task.cast_kwargs, **kwargs}
            return signature(
                self.dependent_task.task, args=self.dependent_task.cast_args, kwargs=kwargs, immutable=True
            )
        return None

    def chord(self, **kwargs: Any) -> chord:
        """
        This function is the main entry point of the synchronization worklow. It is called from within the shared_task `task`
        and create the celery chord containing the list of tasks chained to the end task (if any)
        :param kwargs:
        :return: chord
        """
        kwargs = {**kwargs, **self._get_kwargs()}
        tasks = list(self._tasks_signature(**kwargs))
        if end_task := self._end_task_signature(**kwargs):
            return chord(tasks, end_task)
        return group(tasks)


@receiver(post_save, sender="wbportfolio.SynchronizationTask")
@receiver(post_save, sender="wbportfolio.PortfolioSynchronization")
@receiver(post_save, sender="wbportfolio.PriceComputation")
def post_save_synchronization_task(sender, instance: models.Model, created: bool, raw: bool, **kwargs: Any):
    """
    Ensure args attribute contains the necessary arguments to retrieve the calling job from within asynchronous task
    """
    if (created and not raw) or not instance.args:
        content_type = ContentType.objects.get_for_model(instance)
        instance.args = f'["{instance.id}", "{content_type.app_label}", "{content_type.model}"]'
        instance.save()


@shared_task
def task(synchronization_object_id: int, app_label: str, model: str, **kwargs: Any):
    synchronization_object = ContentType.objects.get(app_label=app_label, model=model).get_object_for_this_type(
        id=synchronization_object_id
    )
    synchronization_object.chord(**kwargs).apply_async()
