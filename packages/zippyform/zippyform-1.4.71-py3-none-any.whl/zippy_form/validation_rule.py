import re
from datetime import datetime

from django.core.validators import URLValidator
from django.db.models import Q
from django.core.exceptions import ValidationError

from zippy_form.models import FormSubmissionData
from zippy_form.utils import FORM_SUBMISSION_STATUS, FIELD_TYPES, FIELD_RULES_DATE_FORMAT_ALLOWED, \
    FIELD_RULES_TIME_FORMAT_ALLOWED


def validate_is_empty(value):
    """
    Check if value exists or not
    """
    error = False

    if not value:
        error = True

    return error


def validate_minlength(value, minlength, field_type):
    """
    Check if value is not less than the minimum characters set.
    """
    error = False

    if field_type == FIELD_TYPES[16][0]:
        cleaned_value = re.findall(r'\d+', value)
        formatted_value = ''.join(cleaned_value)
        value = formatted_value

    if len(value) < minlength:
        error = True

    return error


def validate_maxlength(value, maxlength, field_type):
    """
    Check if value is not greater than the maximum characters set.
    """
    error = False

    if field_type == FIELD_TYPES[16][0]:
        cleaned_value = re.findall(r'\d+', value)
        formatted_value = ''.join(cleaned_value)
        value = formatted_value

    if len(value) > maxlength:
        error = True

    return error


def validate_is_url(value):
    """
    Check if value is valid URL.
    """
    error = False
    if value.startswith('www.'):
        value = 'http://' + value
    url_validator = URLValidator(schemes=['http', 'https'])

    try:
        url_validator(value)
    except ValidationError:
        error = True

    return error


def validate_is_unique(value, field_key, field_type, submission_id=None):
    """
    Check if value doesn't exist already.
    """
    error = False

    if field_type == FIELD_TYPES[0][0] or field_type == FIELD_TYPES[1][0] or field_type == FIELD_TYPES[2][0] \
            or field_type == FIELD_TYPES[3][0] or field_type == FIELD_TYPES[4][0] or field_type == FIELD_TYPES[8][0] \
            or field_type == FIELD_TYPES[9][0] or field_type == FIELD_TYPES[11][0] or field_type == FIELD_TYPES[16][0]\
            or field_type == FIELD_TYPES[21][0]:
        # Check value exist already for the "Active" & "Draft" form submission.
        form_submission_data = FormSubmissionData.objects. \
            filter(Q(form_submission__status=FORM_SUBMISSION_STATUS[1][0])
                   | Q(form_submission__status=FORM_SUBMISSION_STATUS[2][0]))

        if submission_id:
            # if submission id available - submitting the edit form
            form_submission_data = form_submission_data.exclude(form_submission=submission_id)

        value_already_exist = form_submission_data.filter(form_field_id=field_key).filter(text_field=value). \
            exists()

        if value_already_exist:
            error = True

    return error


def validate_is_number(value):
    """
    Check if value is number.
    """
    error = False

    if not value.isnumeric():
        error = True

    return error


def validate_min_value(value, min_value):
    """
    Check if value is greater or equal to the minimum value.
    """
    error = False

    if not float(value) >= float(min_value):
        error = True

    return error


def validate_max_value(value, max_value):
    """
    Check if value is less or equal to the maximum value.
    """
    error = False

    if not float(value) <= float(max_value):
        error = True

    return error


def validate_is_email(value):
    """
    Check if value is valid email.
    """
    error = False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, value):
        error = True

    return error


def validate_is_date(value, date_format_allowed):
    """
    Check if value is valid date.
    """
    try:
        date_format_allowed = FIELD_RULES_DATE_FORMAT_ALLOWED[date_format_allowed]
        datetime.strptime(value, date_format_allowed)
        error = False
    except ValueError:
        error = True

    return error


def validate_min_max_selection(value, max_selection_allowed, validate_min, validate_max):
    """
    Check if length of the value matches the max selection allowed & has minimum 1 if the field is required
    """
    error = 0  # 0 indicates no error

    value_length = len(value)

    if validate_min and value_length == 0:
        error = 1
    elif validate_max and len(value) > max_selection_allowed:
        error = 2

    return error


def validate_is_file(field_key, req):
    """
    Check if value is valid file.
    """
    error = False

    uploaded_file = req.FILES.get(field_key, None)

    if not uploaded_file:
        error = True

    return error


def validate_file_extension(uploaded_file, file_extensions_allowed):
    """
    Check if value is valid file.
    """
    error = False

    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == "jpg":
        file_extension = "jpeg"

    if file_extension not in file_extensions_allowed:
        error = True

    return error


def validate_file_size(uploaded_file, max_file_size_allowed):
    """
    Check if file size not greater than allowed file size limit.
    """
    error = False

    max_upload_size = max_file_size_allowed * 1024 * 1024  # MB

    if uploaded_file.size > max_upload_size:
        error = True

    return error


def validate_is_time(value, time_format_allowed):
    """
    Check if value is valid time.
    """
    try:
        date_format_allowed = FIELD_RULES_TIME_FORMAT_ALLOWED[time_format_allowed]
        datetime.strptime(value, date_format_allowed)
        error = False
    except ValueError:
        error = True

    return error
