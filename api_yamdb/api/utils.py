from django.contrib.auth.tokens import default_token_generator


def get_confirmation_code(user):
    return default_token_generator.make_token(user)
