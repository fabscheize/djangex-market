from django.conf import settings
import django.contrib
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from feedback import forms
from feedback import models

__all__ = []

ITEMS_PER_PAGE = 5


def feedback(request):
    template = 'feedback/feedback.html'

    feedback_form = forms.FeedbackForm(request.POST or None)
    feedback_author_form = forms.FeedbackAuthorForm(request.POST or None)
    feedback_file_form = forms.FeedbackFileForm(request.POST or None)

    context = {
        'feedback_author_form': feedback_author_form,
        'feedback_form': feedback_form,
        'feedback_file_form': feedback_file_form,
    }

    if request.method == 'POST' and all(
        form.is_valid()
        for form in (feedback_author_form, feedback_form, feedback_file_form)
    ):
        send_mail(
            subject=_('Ответ по вашему обращению'),
            message=f'{feedback_form.cleaned_data["text"]}',
            from_email=settings.MAIL,
            recipient_list=[feedback_author_form.cleaned_data['mail']],
            fail_silently=True,
        )

        feedback_object = models.Feedback.objects.create(
            **feedback_form.cleaned_data,
        )
        models.FeedbackAuthor.objects.create(
            feedback=feedback_object,
            **feedback_author_form.cleaned_data,
        )
        for file in request.FILES.getlist('files'):
            models.FeedbackFile.objects.create(
                feedback=feedback_object,
                file=file,
            )

        django.contrib.messages.success(
            request,
            _('Ваше обращение успешно отправлено. Спасибо!'),
        )

        return redirect(reverse('feedback:feedback'))

    return render(request, template, context)
