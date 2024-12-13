import factory
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from wbportfolio.models import (
    PortfolioSynchronization,
    PriceComputation,
    SynchronizationTask,
)


class CrontabScheduleFactory(factory.django.DjangoModelFactory):
    hour = factory.Iterator(range(0, 24))
    minute = factory.Iterator(range(0, 60))

    class Meta:
        model = CrontabSchedule


class PeriodicTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PeriodicTask

    name = factory.Sequence(lambda n: f"Synchronization Task {n}")
    crontab = factory.SubFactory(CrontabScheduleFactory)


class SynchronizationTaskFactory(PeriodicTaskFactory):
    class Meta:
        model = SynchronizationTask


class PortfolioSynchronizationFactory(SynchronizationTaskFactory):
    propagate_history = False

    class Meta:
        model = PortfolioSynchronization


class PriceComputationFactory(SynchronizationTaskFactory):
    class Meta:
        model = PriceComputation
