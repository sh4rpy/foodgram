from django.core.mail import send_mail
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    """Форма регистрации"""
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "users/reg.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_mail(
            'Регистрация',
            'Вы успешно прошли регистрацию на сайте Foodgram.',
            'team.foodgram@yandex.ru',
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)
