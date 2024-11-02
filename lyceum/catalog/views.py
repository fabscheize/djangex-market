from django.shortcuts import get_object_or_404, render

import catalog.models

__all__ = []


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
