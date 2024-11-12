import datetime
import random

from django.db import models
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import catalog.models

__all__ = []

ITEMS_PER_PAGE = 5


def item_list(request):
    template = 'catalog/item_list.html'
    items = catalog.models.Item.objects.published()
    context = {'items': items}
    return render(request, template, context)


def item_detail(request, pk):
    template = 'catalog/item.html'
    item = get_object_or_404(
        catalog.models.Item.objects.item_detailed(),
        pk=pk,
    )
    context = {'item': item}
    return render(request, template, context)


def new_list(request):
    template = 'catalog/special.html'
    published = catalog.models.Item.objects.published()
    week_filter = published.filter(
        created__gte=timezone.now() - datetime.timedelta(days=7),
    )
    items_ids = list(
        week_filter.values_list(catalog.models.Item.id.field.name, flat=True),
    )

    try:
        selected = random.sample(items_ids, ITEMS_PER_PAGE)
    except ValueError:
        selected = items_ids

    items = catalog.models.Item.objects.published().filter(pk__in=selected)
    context = {'items': items, 'title': _('Новинки')}
    return render(request, template, context)


def friday_list(request):
    template = 'catalog/special.html'
    published = catalog.models.Item.objects.published()
    updated_on_friday = published.filter(updated__week_day=6)
    items = updated_on_friday.order_by(catalog.models.Item.updated.field.name)
    context = {'items': items[:5], 'title': _('Пятница')}
    return render(request, template, context)


def unverified_list(request):
    template = 'catalog/special.html'
    items = catalog.models.Item.objects.published().filter(
        created__gte=models.F(catalog.models.Item.updated.field.name)
        - datetime.timedelta(seconds=1),
        created__lte=models.F(catalog.models.Item.updated.field.name)
        + datetime.timedelta(seconds=1),
    )
    context = {'items': items, 'title': _('Непроверенное')}
    return render(request, template, context)
