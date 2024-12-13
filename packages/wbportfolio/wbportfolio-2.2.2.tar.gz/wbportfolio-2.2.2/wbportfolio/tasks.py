from contextlib import suppress
from datetime import date, timedelta

from celery import chain, chord
from django.db.models import ProtectedError, Q
from pandas.tseries.offsets import BDay
from tqdm import tqdm
from wbfdm.models import InstrumentPrice
from wbportfolio.models import Portfolio, Trade
from wbportfolio.models.portfolio import propagate_or_update_portfolio_assets_as_task
from wbportfolio.models.products import Product, update_outstanding_shares_as_task

from .fdm.tasks import *  # noqa


@shared_task()
def dummy_task():
    return True


@shared_task(queue="portfolio")
def periodically_update_outstanding_shares_for_active_products():
    qs = Product.active_objects.all()
    for product in tqdm(qs, total=qs.count()):
        update_outstanding_shares_as_task(product.id)


@shared_task(queue="portfolio")
def periodically_clean_marked_for_deletion_trades(max_allowed_iterations: int = 5):
    # Get all trade marked for deletion or pending and older than 7 days (i.e. After 7 days, we consider the pending trade obselete)
    qs = Trade.objects.filter(
        Q(marked_for_deletion=True) | (Q(pending=True) & Q(transaction_date__lt=date.today() - timedelta(days=7)))
    )
    i = 0

    # We try several times in case the trades deletion mechanism shifts the marked for deletion tag forwards
    while i < max_allowed_iterations and qs.exists():
        for t in qs:
            with suppress(ProtectedError):
                t.delete()
        qs = Trade.objects.filter(marked_for_deletion=True)
        i += 1


# Daily synchronization tasks.
# This tasks needs to be ran at maximum once a day in order to guarantee data consitency in
# case of change in change (e.g. reimport).
@shared_task(queue="portfolio")
def daily_instrument_price_statistics_synchronization(today: date = None, day_periods: int = 7):
    if not today:
        today = date.today()

    # We query for the last 7 days unsynch instrument prices.
    prices = (
        InstrumentPrice.objects.filter(
            date__gte=today - timedelta(days=day_periods), instrument__related_instruments__isnull=False
        )
        .filter(Q(sharpe_ratio__isnull=True) | Q(correlation__isnull=True) | Q(beta__isnull=True))
        .distinct()
    )
    objs = []
    for p in prices.iterator():
        p.compute_and_update_statistics()
        objs.append(p)
    InstrumentPrice.objects.bulk_update(objs, fields=["sharpe_ratio", "correlation", "beta"])


# A Task to run every day to update automatically the preferred classification
# per instrument of each wbportfolio containing assets.
@shared_task(queue="portfolio")
def update_preferred_classification_per_instrument_and_portfolio_as_task():
    for portfolio in Portfolio.tracked_objects.all():
        portfolio.update_preferred_classification_per_instrument()


# This task needs to run at fix interval. It will trigger the basic wbportfolio synchronization update:
# - Fetch for stainly price at t-1
# - propagate (or update) t-2 asset positions into t-1
# - Synchronize wbportfolio at t-1
# - Compute Instrument Price estimate at t-1


@shared_task(queue="portfolio")
def general_portfolio_synchronization_and_update(task_date=None):
    if not task_date:
        task_date = date.today()
    t_1 = (task_date - BDay(1)).date()
    t_2 = (t_1 - BDay(1)).date()

    # We propagate or update assets position from t-2 to t-1 (Needs stainly t-1 prices)
    subroutines_propagate_or_update_portfolio_assets = list()
    for portfolio in Portfolio.tracked_objects.all():
        if (
            portfolio.assets.filter(date=t_2).exists()
            and not portfolio.assets.filter(date=t_1, is_estimated=False).exists()
        ):
            subroutines_propagate_or_update_portfolio_assets.append(
                propagate_or_update_portfolio_assets_as_task.si(portfolio.id, t_2, t_1)
            )

    # # Synchronize wbportfolio at t-1 (needs propagated data)
    # subroutines_synchronize_computed_positions = list()
    # for method in PortfolioSynchronization.objects.all():
    #     for portfolio in method.portfolios.all():
    #         subroutines_synchronize_computed_positions.append(
    #             synchronize_portfolio_as_task.si(portfolio.id, t_1, synchronization_method_id=method.id)
    #         )
    #
    # # Compute price estimate at t-1 (needs synchronized wbportfolio)
    # subroutines_compute_price = list()
    # for method in PriceComputation.objects.all():
    #     for instrument in method.instruments.all():
    #         subroutines_compute_price.append(
    #             compute_price_as_task.si(instrument.id, t_1, price_computation_method_id=method.id)
    #         )

    subroutines_propagate_or_update_portfolio_assets_group = chord(
        subroutines_propagate_or_update_portfolio_assets, dummy_task.si()
    )

    chain(
        subroutines_propagate_or_update_portfolio_assets_group,
        # subroutines_synchronize_computed_positions_group,
        # subroutines_compute_price_group
    ).apply_async()
