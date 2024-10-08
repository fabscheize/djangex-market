import re

from django.conf import settings


def reverse(m: re.Match):
    return m.group(0)[::-1]


class ReverseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.count = 0

    def __call__(self, request):
        response = self.get_response(request)
        self.count += 1

        if self.count == 10:
            self.count = 0
            if settings.ALLOW_REVERSE:
                content = response.content.decode('utf-8')
                reversed_content = re.sub(r'[А-Яа-яёЁ]+', reverse, content)
                response.content = reversed_content.encode('utf-8')
                return response

        return response
