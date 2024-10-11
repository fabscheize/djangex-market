import re

from django.conf import settings


def reverse(m: re.Match):
    return m.group(0)[::-1]


class ReverseMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.ALLOW_REVERSE:
            ReverseMiddleware.count += 1

            if ReverseMiddleware.count == 10:
                ReverseMiddleware.count = 0
                content = response.content.decode('utf-8')
                reversed_content = re.sub(r'[А-Яа-яёЁ]+', reverse, content)
                response.content = reversed_content.encode('utf-8')

        return response
