from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from users import forms, models

__all__ = []


def send_activation_email(request, username):
    user = models.User.objects.get(username=username)
    activation_url = request.build_absolute_uri(
        reverse(
            'users:activate',
            args=[user.username],
        ),
    )
    send_mail(
        subject=_('Подтверждение регистрации'),
        message=_('Для активации перейдите по ссылке: ') + f'{activation_url}',
        from_email=settings.MAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    messages.success(
        request,
        _(
            'Чтобы активировать свой аккаунт перейдите по ссылке '
            'в отправленном нами письме',
        ),
    )
    return redirect(reverse('users:signup'))


def signup(request):
    template = 'users/signup.html'
    form = forms.UserCreationForm(request.POST or None)
    context = {'form': form}

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        if user.is_active:
            return redirect(reverse('users:profile'))

        messages.success(
            request,
            _('Регистрация завершена.'),
        )
        return redirect(reverse('users:send_mail', args=[user.username]))

    return render(request, template, context)


def activate(request, username):
    user = models.User.objects.get(username=username)
    time_elapsed = timezone.now() - user.date_joined

    if time_elapsed <= timezone.timedelta(hours=12):
        user.is_active = True
        user.save()
        messages.success(
            request,
            _(
                'Активация прошла успешно! '
                'Теперь Вы можете войти в свой аккаунт',
            ),
        )
    else:
        activation_path = reverse('users:send_mail', args=[user.username])
        messages.error(
            request,
            mark_safe(
                _('Ссылка активации истекла :(') + '<br><a href='
                f'"{activation_path}"'
                ' class="alert-link">Отправить еще раз</a>',
            ),
        )

    return redirect(reverse('users:login'))


@login_required
def profile(request):
    template = 'users/profile.html'
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = forms.UserChangeForm(
            request.POST,
            instance=user,
        )
        profile_form = forms.ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Профиль обновлен успешно!'))
            return redirect(reverse('users:profile'))
    else:
        user_form = forms.UserChangeForm(instance=user)
        profile_form = forms.ProfileForm(instance=profile)

    context = {
        'forms': [user_form, profile_form],
        'coffee_count': profile.coffee_count,
    }

    return render(request, template, context)


def user_list(request):
    template = 'users/user_list.html'
    context = {
        'users': models.User.objects.filter(is_active=True).select_related(
            'profile',
        ),
    }

    return render(request, template, context)


def user_detail(request, pk):
    template = 'users/user_detail.html'
    user = get_object_or_404(
        models.User.objects.filter(is_active=True).select_related('profile'),
        pk=pk,
    )
    context = {'user_detail': user}

    return render(request, template, context)
