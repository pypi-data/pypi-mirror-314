import uuid

from django.db import models
from .utils import FORM_STATUS, FIELD_TYPES, FORM_FIELD_STATUS, FORM_SUBMISSION_STATUS, FIELD_SIZE, FORM_STEP_STATUS, \
    FORM_FIELD_OPTION_STATUS, ACCOUNT_STATUS, WEBHOOK_STATUS, PAYMENT_TYPE, PAYMENT_MODE, FORM_TYPE, PAYMENT_GATEWAYS, \
    FORM_META_DATA_TYPE, FORM_META_DATA_STATUS, FORM_META_DATA_OPTION_STATUS, GSHEET_MAPPING_FIELDS_STATUS, GSHEET_TYPES


class Account(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    admin_email = models.CharField(max_length=255, blank=True, default="")
    timezone = models.CharField(max_length=255, blank=True, default="")
    meta_detail = models.CharField(max_length=255, blank=True, default="")
    is_payment_collect_enabled = models.BooleanField(default=False)
    primary_payment_gateway = models.CharField(max_length=255, default=PAYMENT_GATEWAYS[0][0], blank=True)
    status = models.CharField(max_length=10, choices=ACCOUNT_STATUS, default=ACCOUNT_STATUS[1][0])
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class AccountPaymentSettings(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_payment_settings")
    payment_gateway = models.CharField(max_length=255)
    payment_mode = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Form(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    class_name = models.CharField(max_length=255, blank=True)
    success_msg = models.TextField(blank=True)
    meta_detail = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=10, choices=FORM_STATUS, default=FORM_STATUS[3][0])
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account")
    gsheet_url = models.CharField(max_length=255, blank=True, default="")
    qrcode = models.FileField(null=True, default=None)
    non_admin_qrcode = models.FileField(null=True, default=None)
    type = models.CharField(max_length=255, blank=True, default=FORM_TYPE[0][0])
    category = models.CharField(max_length=255, blank=True)
    primary_payment_mode = models.CharField(max_length=255, default=PAYMENT_MODE[0][0])
    gsheet_type = models.CharField(max_length=255, choices=GSHEET_TYPES, default=GSHEET_TYPES[0][0])
    multi_step = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class FormMetaData(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255)
    meta_label = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=FORM_META_DATA_TYPE, default=FORM_META_DATA_TYPE[0][0])
    status = models.CharField(max_length=10, choices=FORM_META_DATA_STATUS, default=FORM_META_DATA_STATUS[1][0])
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class FormMetaDataOption(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    form_meta_data = models.ForeignKey(FormMetaData, on_delete=models.CASCADE)
    option = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=FORM_META_DATA_OPTION_STATUS,
                              default=FORM_META_DATA_OPTION_STATUS[1][0])
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class FormSettings(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="form_settings")
    recaptcha_enabled = models.BooleanField(default=False)
    site_key = models.CharField(max_length=255, null=True)
    secret_key = models.CharField(max_length=255, null=True)
    gsheet_enabled = models.BooleanField(default=False)
    gsheet_type = models.CharField(max_length=255, choices=GSHEET_TYPES, default=GSHEET_TYPES[0][0], null=True)


class FormStep(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="form_steps")
    step_order = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=FORM_STEP_STATUS, default=FORM_STEP_STATUS[1][0])


class FormField(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    label = models.CharField(max_length=255, default="Untitled")
    slug = models.CharField(max_length=255, default="", blank=True)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    field_size = models.CharField(max_length=20, choices=FIELD_SIZE, default=FIELD_SIZE[0][0])
    placeholder = models.CharField(max_length=255, blank=True)
    field_order = models.PositiveIntegerField()
    custom_class_name = models.CharField(max_length=255, blank=True)
    validation_rule = models.JSONField(default=dict)
    field_format = models.JSONField(default=dict)
    is_mandatory = models.BooleanField(default=False) # Admin Only Delete
    system_field = models.BooleanField(default=False)
    admin_only_edit = models.BooleanField(default=False) # Admin Only Edit
    admin_can_submit = models.BooleanField(default=True) # Admin Can Submit
    user_can_submit = models.BooleanField(default=True) # User Can Submit
    is_unique = models.BooleanField(default=False)
    admin_show_on_table = models.BooleanField(default=True)
    user_show_on_table = models.BooleanField(default=True)
    table_field_order = models.PositiveIntegerField(default=0)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="form_fields")
    form_step = models.ForeignKey(FormStep, on_delete=models.CASCADE, related_name="form_step_fields")
    status = models.CharField(max_length=10, choices=FORM_FIELD_STATUS, default=FORM_FIELD_STATUS[3][0])
    is_field_settings_updated = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    content_size = models.CharField(blank=True, max_length=255)
    content_alignment = models.CharField(blank=True, max_length=255)
    option_api_url = models.CharField(blank=True, max_length=255, null=True)
    option_api_detail_url = models.CharField(blank=True, max_length=255, null=True)
    starts_from = models.PositiveIntegerField(default=0)
    prefix = models.CharField(blank=True, max_length=255)
    suffix = models.CharField(blank=True, max_length=255)


# Use 'FormFieldOption' table for saving dropdown, radio, checkbox options
class FormFieldOption(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    label = models.CharField(max_length=255)
    option_order = models.PositiveIntegerField(default=0)
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE, related_name="form_field_options")
    status = models.CharField(max_length=10, choices=FORM_FIELD_OPTION_STATUS, default=FORM_FIELD_OPTION_STATUS[1][0])

class FormFieldDropdownOption(models.Model):
   id = models.UUIDField(
       primary_key=True,
       default=uuid.uuid4,
       editable=False)
   option_id = models.CharField(max_length=255)
   option_value = models.CharField(max_length=255)
   status = models.CharField(max_length=10, choices=FORM_FIELD_OPTION_STATUS, default=FORM_FIELD_OPTION_STATUS[1][0])

class FormPageViews(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class FormSubmission(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=FORM_SUBMISSION_STATUS, default=FORM_SUBMISSION_STATUS[2][0])
    submission_sequence = models.PositiveIntegerField(default=1)
    user_agent = models.CharField(max_length=255, blank=True)
    request_ip = models.CharField(max_length=255, blank=True)
    revision = models.PositiveIntegerField(default=1)
    api_accessed_count = models.PositiveIntegerField(default=1)
    submission_owner = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

class FormSubmissionData(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    form_submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=FORM_SUBMISSION_STATUS, default=FORM_SUBMISSION_STATUS[2][0])
    submission_sequence = models.PositiveIntegerField(default=1)
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE, null=True)
    form_field_type = models.CharField(max_length=255, blank=True)
    text_field = models.TextField(blank=True)
    checkbox_field = models.BooleanField(blank=True, null=True)
    multiselect_checkbox_field = models.JSONField(null=True, default=None)
    radio_field = models.CharField(max_length=255, blank=True)
    dropdown_field = models.JSONField(null=True, default=None)
    location_field = models.JSONField(null=True, default=None)
    date_field = models.DateField(blank=True,null=True,default=None)
    file_field = models.FileField(blank=True)
    unique_field = models.TextField(blank=True)
    submission_reference = models.CharField(max_length=255, blank=True)

class FormSubmissionPaymentDetails(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    form_submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE)
    payment_gateway = models.CharField(max_length=255, default=PAYMENT_GATEWAYS[0][0])
    payment_type = models.CharField(max_length=255, default=PAYMENT_TYPE[0][0])
    payment_mode = models.CharField(max_length=255, default=PAYMENT_MODE[0][0])
    currency = models.CharField(max_length=255, blank=True)
    sub_total = models.CharField(max_length=255)  # Price entered on the Payment Settings
    tax_percentage = models.CharField(max_length=255, blank=True)
    tax_amount = models.CharField(max_length=255, blank=True)
    total = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class FormSubmissionMetaDataValue(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    form_submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE)
    form_meta_data = models.ForeignKey(FormMetaData, on_delete=models.CASCADE)
    form_meta_data_type = models.CharField(max_length=255, choices=FORM_META_DATA_TYPE,
                                           default=FORM_META_DATA_TYPE[0][0])
    text_field = models.TextField(blank=True)
    dropdown_field = models.ForeignKey(FormMetaDataOption, on_delete=models.CASCADE, null=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class FormPaymentSettings(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="form_payment_settings")
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # Form account id
    payment_gateway = models.CharField(max_length=255, blank=True, default="")
    payment_type = models.CharField(max_length=255, default=PAYMENT_TYPE[0][0])
    payment_mode = models.CharField(max_length=255, default=PAYMENT_MODE[0][0])
    currency = models.CharField(max_length=255, blank=True)
    price = models.TextField(blank=True)
    dynamic_price_field = models.ForeignKey(FormField, on_delete=models.CASCADE, null=True)
    tax_enabled = models.BooleanField(default=False)
    tax = models.CharField(max_length=255, blank=True)
    tax_display_name = models.CharField(max_length=255, blank=True)
    stripe_product_id = models.CharField(max_length=255, blank=True)
    stripe_price_id = models.CharField(max_length=255, blank=True)
    stripe_tax_rate_id = models.CharField(max_length=255, blank=True)
    redirect_url = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Webhook(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    endpoint_url = models.URLField()
    description = models.TextField(blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    event_new_form_created = models.BooleanField(default=False)
    event_form_submit = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=WEBHOOK_STATUS, default=WEBHOOK_STATUS[1][0])
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class WebhookForm(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE, related_name='webhook_form')
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    event_new_form_created = models.BooleanField(default=False)
    event_form_submit = models.BooleanField(default=False)


class PaymentGatewayWebhook(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    payment_gateway = models.CharField(max_length=255)
    payment_mode = models.CharField(max_length=255)
    webhook_reference_id = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class GoogleCredentials(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='account_credentials')
    credentials = models.JSONField(default=dict, null=True)
    is_config_done = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class GsheetMappingFields(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='gsheet_mapping_fields')
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE, related_name="gsheet_mapping_form_fields", null=True)
    gsheet_column_name = models.CharField(max_length=255, blank=True)
    form_field_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=GSHEET_MAPPING_FIELDS_STATUS, default=GSHEET_MAPPING_FIELDS_STATUS[1][0])
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class GSheetSyncFields(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='gsheet_sync_form')
    form_field = models.ForeignKey(FormField, on_delete=models.CASCADE, related_name="gsheet_sync_fields")
    gsheet_type = models.CharField(max_length=255, choices=GSHEET_TYPES, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class FormGsheetMappingHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='gsheet_mapping_history')
    zf_gsheet_url = models.CharField(max_length=255, blank=True)
    custom_gsheet_url = models.CharField(max_length=255, blank=True)
    custom_existing_gsheet_url = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)