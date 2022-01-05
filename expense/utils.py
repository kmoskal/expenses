from rest_framework import exceptions
from datetime import datetime

MIN_YEAR = datetime.min.year
MAX_YEAR = datetime.max.year
MIN_MONTH = datetime.min.month
MAX_MONTH = datetime.max.month
MIN_DAY = datetime.min.day
MAX_DAY = datetime.max.day


def create_date_form_query_param(
        min_value, max_value,
        to_date=False, query_value=None
):
    if query_value:
        if min_value <= int(query_value) <= max_value:
            return query_value
        else:
            raise exceptions.ValidationError(
                {'detail': 'Out of range'}
            )
    else:
        if max_value == MAX_YEAR:
            return datetime.now().year
        if max_value == MAX_MONTH:
            return datetime.now().month
        if max_value == MAX_DAY:
            if to_date:
                return max_value
            else:
                return min_value


def create_date_range(query_params):
    from_year = create_date_form_query_param(
        MIN_YEAR, MAX_YEAR,
        query_value=query_params.get('fyear')
    )

    from_month = create_date_form_query_param(
        MIN_MONTH, MAX_MONTH,
        query_value=query_params.get('fmonth')
    )

    from_day = create_date_form_query_param(
        MIN_DAY, MAX_DAY,
        query_value=query_params.get('fday')
    )

    to_year = create_date_form_query_param(
        MIN_YEAR, MAX_YEAR, True,
        query_value=query_params.get('tyear')
    )

    to_month = create_date_form_query_param(
        MIN_MONTH, MAX_MONTH, True,
        query_value=query_params.get('tmonth')
    )

    to_day = create_date_form_query_param(
        MIN_DAY, MAX_DAY, True,
        query_value=query_params.get('tday')
    )

    from_date = datetime(int(from_year), int(from_month), int(from_day))
    to_date = datetime(int(to_year), int(to_month), int(to_day))

    if from_date > to_date:
        raise exceptions.ValidationError(
            {'detail': 'Start date is newer then end date'}
        )
    else:
        return [str(from_date.date()), str(to_date.date())]
