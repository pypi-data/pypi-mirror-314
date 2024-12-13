from datetime import date

from celery import shared_task
from django.db import transaction
from django.db.models import Q
from pandas.tseries.offsets import BDay
from tqdm import tqdm
from wbfdm.models import Instrument
from wbfdm.sync.runner import (  # noqa: F401
    initialize_exchanges,
    initialize_instruments,
    synchronize_exchanges,
    synchronize_instruments,
)


@shared_task(queue="portfolio")
def update_of_investable_universe_data(start: date | None = None, end: date | None = None, clear: bool = False):
    """
    Update the investable universe data on a daily basis.

    Parameters:
    - start (date | None): The start date for updating data. If None, defaults to three business days before 'end'.
    - end (date | None): The end date for updating data. If None, defaults to the current date.

    Notes:
    - The function resets the investable universe by marking all instruments as not in the investable universe.
    - It then updates all instruments marked as part of the investable universe.
    - If 'end' is not provided, it defaults to the current date.
    - If 'start' is not provided, it defaults to three business days before 'end'.

    Returns:
    None
    """
    if not end:
        end = (
            date.today() - BDay(1)
        ).date()  # we don't import today price in case the dataloader returns duplicates (e.g. DSWS)
    if not start:
        start = (end - BDay(3)).date()  # override three last day by default

    Instrument.investable_universe.update(
        is_investable_universe=True
    )  # ensure all the investable universe is marked as such

    instruments = Instrument.active_objects.filter(is_investable_universe=True, delisted_date__isnull=True).exclude(
        Q(is_managed=True)
        | Q(dl_parameters__market_data__path="wbfdm.contrib.internal.dataloaders.market_data.MarketDataDataloader")
    )  # we exclude product and index managed to avoid circular import
    for instrument in tqdm(instruments, total=instruments.count()):
        instrument.import_prices(start=start, end=end, clear=clear)


@shared_task(queue="portfolio")
def synchronize_instruments_as_task():
    synchronize_instruments()


@shared_task(queue="portfolio")
def synchronize_exchanges_as_task():
    synchronize_exchanges()


@shared_task(queue="portfolio")
def full_synchronization_as_task():
    initialize_exchanges()
    initialize_instruments()
    with transaction.atomic():
        Instrument.objects.rebuild()  # rebuild MPTT tree
