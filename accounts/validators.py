from django.core.exceptions import ValidationError
from django.utils.translation import ngettext


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
                ngettext(
                    'Password must contains at least %(mdn)d digit.',

                    'Password must contains at least %(mdn)d digits.',
                    self.min_digits_number,
                ) % {
                    'mdn': self.min_digits_number,
                }
            )

        def get_help_text(self):
            return ngettext(
                'Password mustt contains at least %(mdn)d digit.',
                'Password mustt contains at least %(mdn)d digits.',
                self.min_digits_number,
            ) % {'mdn': self.min_digits_number, }
