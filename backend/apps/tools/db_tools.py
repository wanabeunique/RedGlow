from channels.db import database_sync_to_async
from django.db.models import Model, BaseManager
from typing import Iterable

@database_sync_to_async
def async_filter_exists(model: Model, *nameless_filters, **filters):
    return model.objects.filter(*nameless_filters, **filters).exists()

@database_sync_to_async
def async_filter_first(model: Model, *nameless_filters, **filters):
    return model.objects.filter(*nameless_filters, **filters).first()

@database_sync_to_async
def async_filter_update(model: Model, *nameless_filters, filters: dict, updates: dict):
    return model.objects.filter(*nameless_filters, **filters).update(**updates)


@database_sync_to_async
def async_filter_delete(model: Model, *nameless_filters, **filters):
    return model.objects.filter(*nameless_filters, **filters).delete()


@database_sync_to_async
def async_filter_values(model: Model, values: Iterable, *nameless_filters, border=None, **filters):
    if border is not None:
        return model.objects.filter(*nameless_filters, **filters).values(*values)[:border]
    return model.objects.filter(*nameless_filters, **filters).values(*values)

@database_sync_to_async
def async_filter_count(model: Model, *nameless_filters, base_manager: BaseManager[Model] | None = None, **filters):
    if base_manager is not None:
        return base_manager.filter(*nameless_filters, **filters).count()
    return model.objects.filter(*nameless_filters, **filters).count()

@database_sync_to_async
def async_filter_select_related(model: Model, 
                                select_related_lst : list[str], 
                                *nameless_filters, 
                                base_manager: BaseManager[Model] | None = None, 
                                **filters):
    if base_manager is not None:
        return base_manager.filter(*nameless_filters, **filters).select_related(*select_related_lst)
    return model.objects.filter(*nameless_filters, **filters).select_related(*select_related_lst)