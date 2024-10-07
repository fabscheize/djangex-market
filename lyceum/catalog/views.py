from django.http import HttpResponse


def item_list(request):
    return HttpResponse('<body>Список элементов</body>')


def item_detail(request, id):
    return HttpResponse(f'<body>Подробно элемент #{id}</body>')
