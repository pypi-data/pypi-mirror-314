import datetime
import pytz
import qrcode
import os
from django.conf import settings
from django.core.files.storage import default_storage

APPLICATION_TYPE = (
    ('standalone', 'Standalone'),
    ('saas', 'SaaS'),
)

ACCOUNT_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
)

ACCOUNT_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
}

CURRENCY_DETAILS = {
    'inr': "INR",
    'usd': "USD"
}

DEFAULT_STRIPE_APPLICATION_FEE_AMOUNT = 0

FORM_TYPE = (
    ('standard_form', 'Standard Form'),
    ('payment_form', 'Payment Form'),
)

FORM_TYPE_DETAILS = {
    'standard_form': 'Standard Form',
    'payment_form': 'Payment Form',
}

FORM_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
    ('in_active', 'InActive'),
    ('draft', 'Draft'),
    ('archive', 'Archive'),
)

FORM_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
    'in_active': 'InActive',
    'draft': 'Draft',
    'archive': 'Archive',
}

FORM_META_DATA_OPTION_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
    ('in_active', 'InActive'),
)

FORM_META_DATA_OPTION_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
    'in_active': 'InActive',
}

FORM_META_DATA_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
    ('in_active', 'InActive'),
)

FORM_META_DATA_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
    'in_active': 'InActive',
}

FORM_META_DATA_TYPE = (
    ('text', 'Text'),
    ('dropdown', 'Dropdown'),
)

FORM_META_DATA_TYPE_DETAILS = {
    'text': 'Text',
    'dropdown': 'Dropdown',
}

FORM_STEP_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
)

FORM_STEP_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
}

FORM_FIELD_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
    ('in_active', 'InActive'),
    ('draft', 'Draft'),
)

FORM_FIELD_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
    'in_active': 'InActive',
    'draft': 'Draft',
}

FORM_FIELD_OPTION_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
)

FORM_SUBMISSION_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
    ('draft', 'Draft'),
    ('payment_pending', 'Payment Pending'),
)

FORM_SUBMISSION_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
    'draft': 'Draft',
    'payment_pending': 'Payment Pending',
}

FIELD_SIZE = (
    ('col-md-12', 'Large'),
    ('col-md-6', 'Medium'),
    ('col-md-4', 'Small'),
)

FIELD_TYPES = (
    ('text_box', 'Text Box'),
    ('website_url', 'Website URL'),
    ('text_area', 'TextArea'),
    ('number', 'Number'),
    ('email', 'Email'),
    ('dropdown', 'Dropdown'),
    ('radio', 'Radio'),
    ('checkbox', 'Checkbox'),
    ('date', 'Date'),
    ('time', 'Time'),
    ('file', 'File Upload'),
    ('short_text_area', 'Short TextArea'),
    ('multiselect_checkbox', 'MultiSelect Checkbox'),
    ('hidden', 'Hidden'),
    ('heading', 'Heading'),
    ('paragraph', 'Paragraph'),
    ('phone_number', 'Phone Number'),
    ('dynamic_dropdown', 'Dynamic Dropdown'),
    ('image', 'Image'),
    ('signature', 'Signature'),
    ('location', 'Location'),
    ('unique_id', 'Unique ID')
)

FIELD_RULES = (
    ('required', 'Required'),
    ('minlength', 'MinLength'),
    ('maxlength', 'MaxLength'),
    ('min', 'Min'),
    ('max', 'Max'),
    ('email', 'Email'),
    ('url', 'URL'),
    ('date', 'Date'),
    ('unique', 'Unique'),
    ('number', 'Number'),
    ('max_selection', 'Max Selection'),
    ('file', 'File'),
    ('time', 'Time'),
    ('image', 'Image'),
)

FIELD_RULES_DATE_FORMAT_ALLOWED = {
    'm-d-Y': '%m-%d-%Y',
    'd-m-Y': '%d-%m-%Y'
}

FIELD_RULES_TIME_FORMAT_ALLOWED = {
    '12': '%I:%M %p',
    '24': '%H:%M'
}

FIELD_RULES_FILE_FORMAT_ALLOWED = ["jpg", "jpeg", "png", "doc", "pdf"]

FIELD_RULES_IMAGE_FORMAT_ALLOWED = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "heif", "raw", "svg"]

PAYMENT_GATEWAYS = (
    ('stripe', 'Stripe'),
)

PAYMENT_TYPE = (
    ('fixed_price', 'Fixed Price'),
    ('dynamic_price', 'Dynamic Price'),
)

PAYMENT_TYPE_DETAILS = {
    'fixed_price': 'Fixed Price',
    'dynamic_price': 'Dynamic Price',
}

PAYMENT_MODE = (
    ('test', 'Test'),
    ('live', 'Live'),
)

PAYMENT_MODE_DETAILS = {
    'test': 'Test',
    'live': 'Live',
}

WEBHOOK_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
    ('in_active', 'InActive'),
)

WEBHOOK_STATUS_DETAILS = {
    'deleted': 'Deleted',
    'active': 'Active',
    'in_active': 'InActive',
}

GSHEET_TYPES = (
    ('zippy_form_spreadsheet', 'ZIPPY FORM SPREADSHEET'),
    ('custom_new_spreadsheet', 'CUSTOM NEW SPREADSHEET'),
    ('custom_existing_spreadsheet', 'CUSTOM EXISTING SPREADSHEET')
)

GSHEET_MAPPING_FIELDS_STATUS = (
    ('deleted', 'Deleted'),
    ('active', 'Active'),
    ('in_active', 'InActive')
)


def generate_url_qrcode(form_id, url, name):
    """
    Generate QR Code with URL
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    form_id = str(form_id)
    media_root = settings.MEDIA_ROOT
    image_path = os.path.join(media_root, name)

    with default_storage.open(image_path, 'wb') as img_file:
        img.save(img_file)

    return image_path


def convert_utc_to_timezone(utc_datetime_str, target_timezone_str):
    """
    Concert UTC Time To User Account TimeZone
    """
    # Parse the UTC datetime string into a datetime object
    utc_datetime = datetime.datetime.strptime(utc_datetime_str, "%Y-%m-%d %H:%M:%S.%f%z")

    # Convert the UTC datetime object to the target timezone
    target_timezone = pytz.timezone(target_timezone_str)
    target_datetime = utc_datetime.astimezone(target_timezone)

    return target_datetime


def format_form_submission_status(form_submission_status, form_type):
    """
    Format Form Submission Status
    """
    status_mapping = {
        'standard_form': {},
        'payment_form': {}
    }

    status_mapping['standard_form']['deleted'] = 'Deleted'
    status_mapping['standard_form']['draft'] = 'Partially Submitted'
    status_mapping['standard_form']['active'] = 'Submitted'

    status_mapping['payment_form']['deleted'] = 'Deleted'
    status_mapping['payment_form']['draft'] = 'Partially Submitted'
    status_mapping['payment_form']['payment_pending'] = 'Payment Pending'
    status_mapping['payment_form']['active'] = 'Payment Completed'

    return status_mapping[form_type][form_submission_status]


def get_stripe_secret_key(payment_mode):
    """
    Get Stripe Secret Key Based On The Payment Mode
    """
    secret_key = ""
    if payment_mode == PAYMENT_MODE[0][0]:
        secret_key = getattr(settings, 'ZF_PAYMENT_GATEWAY_STRIPE_SECRET_KEY_DEV', "")
    elif payment_mode == PAYMENT_MODE[1][0]:
        secret_key = getattr(settings, 'ZF_PAYMENT_GATEWAY_STRIPE_SECRET_KEY_LIVE', "")

    return secret_key


def get_stripe_public_key(payment_mode):
    """
    Get Stripe Public Key Based On The Payment Mode
    """
    public_key = ""
    if payment_mode == PAYMENT_MODE[0][0]:
        public_key = getattr(settings, 'ZF_PAYMENT_GATEWAY_STRIPE_PUBLIC_KEY_DEV', "")
    elif payment_mode == PAYMENT_MODE[1][0]:
        public_key = getattr(settings, 'ZF_PAYMENT_GATEWAY_STRIPE_PUBLIC_KEY_LIVE', "")

    return public_key


def get_stripe_connect_url(payment_mode):
    """
    Get Stripe Connect Url Based on Payment Mode
    """
    connect_url = ''
    if payment_mode == PAYMENT_MODE[0][0]:
        connect_url = getattr(settings, 'ZF_PAYMENT_GATEWAY_STRIPE_CONNECT_URL_DEV', "")
    else:
        connect_url = getattr(settings, 'ZF_PAYMENT_GATEWAY_STRIPE_CONNECT_URL_LIVE', "")

    return connect_url


def check_key_exists_on_dict(dict, key):
    """
    Check Key Exists On Dict
    """
    if key in dict.keys():
        return True
    else:
        return False


"""
DEV NOTES:

* When adding new payment gateway to the package, search for the below comment on "views.py" to add the new payment gateway logics.
    # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here
    
"""
