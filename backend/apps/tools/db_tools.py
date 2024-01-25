from channels.db import database_sync_to_async
from django.db.models import Model
from typing import Iterable


@database_sync_to_async
def async_filter_exists(model: Model, *nameless_filters, **filters):
    return model.objects.filter(*nameless_filters, **filters).exists()


@database_sync_to_async
def async_filter_update(model: Model, *nameless_filters, filters: dict, updates: dict):
    return model.objects.filter(*nameless_filters, **filters).update(**updates)


@database_sync_to_async
def async_filter_delete(self, model: Model, *nameless_filters, **filters):
    return model.objects.filter(*nameless_filters, **filters).delete()


@database_sync_to_async
def async_filter_values(self, model: Model, values: Iterable, *nameless_filters, border=None, **filters):
    if border is not None:
        return model.objects.filter(*nameless_filters, **filters).values(*values)[:border]
    return model.objects.filter(*nameless_filters, **filters).values(*values)
