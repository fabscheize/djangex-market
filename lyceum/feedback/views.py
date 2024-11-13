from django.conf import settings
import django.contrib
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from feedback.forms import FeedbackForm
from feedback.models import Feedback

__all__ = []

ITEMS_PER_PAGE = 5


def feedback(request):
    template = 'feedback/feedback.html'
    feedback_form = FeedbackForm(request.POST or None)
    context = {
        'feedback_form': feedback_form,
    }

    if request.method == 'POST' and feedback_form.is_valid():
        send_mail(
            subject=_('Ответ по вашему обращению'),
            message=f'{feedback_form.cleaned_data["text"]}',
            from_email=settings.MAIL,
            recipient_list=[feedback_form.cleaned_data['mail']],
            fail_silently=False,
        )

        Feedback.objects.create(**feedback_form.cleaned_data)

        django.contrib.messages.success(
            request,
            _('Ваше обращение успешно отправлено. Спасибо!'),
        )

        return redirect(reverse('feedback:feedback'))

    return render(request, template, context)
