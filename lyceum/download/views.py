from django.conf import settings
from django.http import FileResponse

__all__ = []


def get_file(request, path):
    return FileResponse(
        open(settings.MEDIA_ROOT / path, 'rb'),
        as_attachment=True,
    )
