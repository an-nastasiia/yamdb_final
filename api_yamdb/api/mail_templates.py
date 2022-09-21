from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_confirm_mail(user):
    """Send confirmation email to specified user."""
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        f'Код подтверждения для {settings.PROJECT_NAME}',
        f'Код подтверждения для {user.username}: {confirmation_code}',
        settings.PROJECT_MAIL,
        [user.email],
        fail_silently=False,
    )
