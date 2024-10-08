import re

from django.conf import settings


def reverse(m: re.Match):
    return m.group(0)[::-1]


class ReverseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        count = request.session.get('reverse_count', 0)
        count += 1
        request.session['reverse_count'] = count

        if count == 10:
            request.session['reverse_count'] = 0
            if settings.ALLOW_REVERSE:
                content = response.content.decode('utf-8')
                reversed_content = re.sub(r'[А-Яа-яёЁ]+', reverse, content)
                response.content = reversed_content.encode('utf-8')
                return response

        return response
