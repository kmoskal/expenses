from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class MinimumDigitsNumberValidator:
    def __init__(self, min_digits_number=1):
        self.min_digits_number = min_digits_number

    def validate(self, password, user=None):
        count = 0
        for char in password:
            if char.isdigit():
                count += 1

        if count < self.min_digits_number:
            raise ValidationError(
                _(
                    f'Password must contains at least '
                    f'{self.min_digits_number} digit.'
                ),
                code='not enough digits',
            )

        def get_help_text(self):
            return _(
                f'Your password must contain at least '
                f'{self.min_digits_number} digit.'
            )
