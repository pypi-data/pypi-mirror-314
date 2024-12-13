from django.db.models.signals import ModelSignal

# this signal is triggered by the investable universe manager in order to gather what instrument are considered within the investable universe.
add_instrument_to_investable_universe = ModelSignal(use_caching=False)

# this signal is triggered whenever prices are stored in the system and action needs to be considered
instrument_price_imported = ModelSignal(use_caching=False)
