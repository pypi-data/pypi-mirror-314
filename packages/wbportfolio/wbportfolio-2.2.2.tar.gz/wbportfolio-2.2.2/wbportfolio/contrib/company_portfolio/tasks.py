from datetime import date

from celery import shared_task
from tqdm import tqdm
from wbcore.contrib.currency.models import CurrencyFXRates
from wbcore.contrib.directory.models import Company, Entry

from .models import Updater


@shared_task(queue="portfolio")
def update_all_portfolio_data(val_date: date | None = None):
    if not val_date:
        val_date = CurrencyFXRates.objects.latest("date").date
    updater = Updater(val_date)
    account_owners = Entry.objects.filter(accounts__isnull=False)
    qs = Company.objects.filter(id__in=account_owners)
    for company in tqdm(qs, total=qs.count()):
        updater.update_company_data(company)
