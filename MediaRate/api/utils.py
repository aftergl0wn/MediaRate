import uuid
from django.conf import settings


def get_confirmation_code():
    return str(uuid.uuid4()
               ).replace('-', '')[:settings.CONFIRMATION_CODE_LENGTH]
