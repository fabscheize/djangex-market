from django.conf import settings
from django.http import FileResponse, Http404

__all__ = []


def get_file(request, path):
    try:
        response = FileResponse(
            open(settings.MEDIA_ROOT / path, 'rb'),
            as_attachment=True,
        )
    except FileNotFoundError:
        raise Http404('File not found')
    return response
