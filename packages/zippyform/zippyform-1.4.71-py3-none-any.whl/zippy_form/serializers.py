from rest_framework import serializers
from jsonschema import validate, ValidationError
from django.conf import settings

from zippy_form.models import FormStep, FormField, Form, Account, Webhook, FormPaymentSettings
from zippy_form.timezone import ALLOWED_TIME_ZONES
from zippy_form.utils import FIELD_TYPES, FIELD_RULES_DATE_FORMAT_ALLOWED, FIELD_RULES_TIME_FORMAT_ALLOWED, FORM_STATUS, \
    FORM_FIELD_STATUS, PAYMENT_TYPE, PAYMENT_GATEWAYS, APPLICATION_TYPE
from zippy_form.validation_rule_schema import get_text_box_field_validation_rule_schema, \
    get_textarea_field_validation_rule_schema, get_website_url_field_validation_rule_schema, \
    get_short_textarea_field_validation_rule_schema, get_number_field_validation_rule_schema, \
    get_email_field_validation_rule_schema, get_date_field_validation_rule_schema, \
    get_time_field_validation_rule_schema, get_dropdown_field_validation_rule_schema, \
    get_radio_field_validation_rule_schema, get_multiselect_checkbox_field_validation_rule_schema, \
    get_file_field_validation_rule_schema, get_hidden_field_validation_rule_schema, \
    get_phone_no_field_validation_rule_schema, get_dynamic_dropdown_field_validation_rule_schema, \
    get_image_field_validation_rule_schema, get_signature_field_validation_rule_schema, \
    get_location_field_validation_rule_schema, get_unique_id_field_validation_rule_schema


class AccountSerializer(serializers.ModelSerializer):
    def validate_admin_email(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank")
        return value

    def validate_timezone(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank")
        elif value not in ALLOWED_TIME_ZONES:
            raise serializers.ValidationError("Invalid timezone")

        return value

    def validate_primary_payment_gateway(self, value):
        if value:
            is_valid_payment_gateway = False
            for payment_gateway in PAYMENT_GATEWAYS:
                if value == payment_gateway[0]:
                    is_valid_payment_gateway = True
                    break

            if not is_valid_payment_gateway:
                raise serializers.ValidationError("Invalid Payment Gateway")
        else:
            raise serializers.ValidationError("This field may not be blank")

        return value

    def validate(self, attrs):
        application_type = getattr(settings, 'ZF_APPLICATION_TYPE', APPLICATION_TYPE[0][0])
        admin_email_field = attrs.get('admin_email', None)
        timezone_field = attrs.get('timezone', None)
        is_payment_collect_enabled = attrs.get('is_payment_collect_enabled', None)
        primary_payment_gateway = attrs.get('primary_payment_gateway', None)

        if admin_email_field is None:
            raise serializers.ValidationError({"admin_email": ["This field is required"]})

        if timezone_field is None:
            raise serializers.ValidationError({"timezone": ["This field is required"]})

        if is_payment_collect_enabled:
            if primary_payment_gateway is None:
                raise serializers.ValidationError({"primary_payment_gateway": ["This field is required"]})

        return attrs

    class Meta:
        model = Account
        fields = ['id', 'name', 'admin_email', 'timezone', 'meta_detail', 'is_payment_collect_enabled',
                  'primary_payment_gateway']


class AccountPaymentUpdateSerializer(serializers.ModelSerializer):
    def validate_primary_payment_gateway(self, value):
        if value:
            is_valid_payment_gateway = False
            for payment_gateway in PAYMENT_GATEWAYS:
                if value == payment_gateway[0]:
                    is_valid_payment_gateway = True
                    break

            if not is_valid_payment_gateway:
                raise serializers.ValidationError("Invalid Payment Gateway")
        else:
            raise serializers.ValidationError("This field may not be blank")

        return value

    def validate(self, attrs):
        application_type = getattr(settings, 'ZF_APPLICATION_TYPE', APPLICATION_TYPE[0][0])
        is_payment_collect_enabled = attrs.get('is_payment_collect_enabled', None)
        primary_payment_gateway = attrs.get('primary_payment_gateway', None)

        if is_payment_collect_enabled:
            if primary_payment_gateway is None:
                raise serializers.ValidationError({"primary_payment_gateway": ["This field is required"]})

        return attrs

    class Meta:
        model = Account
        fields = ['id', 'is_payment_collect_enabled', 'primary_payment_gateway']


class AccountProfileUpdateSerializer(serializers.ModelSerializer):
    def validate_timezone(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank")
        elif value not in ALLOWED_TIME_ZONES:
            raise serializers.ValidationError("Invalid timezone")

        return value

    def validate(self, attrs):
        timezone_field = attrs.get('timezone', None)

        if timezone_field is None:
            raise serializers.ValidationError({"timezone": ["This field is required"]})

        return attrs

    class Meta:
        model = Account
        fields = ['id', 'name', 'meta_detail', 'timezone']


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id', 'name', 'meta_detail']


class FormStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormStep
        fields = ['id', 'name', 'form']

    def validate_form(self, attrs):
        if attrs.status == FORM_STATUS[0][0]:
            raise serializers.ValidationError('Invalid Form ID.')

        return attrs

    def create(self, validated_data):
        step_order = 1
        last_form_step = FormStep.objects.filter(form_id=validated_data['form']).order_by('-step_order').first()
        if last_form_step:
            last_form_step_order = last_form_step.step_order
            step_order = last_form_step_order + 1

        validated_data['step_order'] = step_order
        return FormStep.objects.create(**validated_data)


class MapFieldToFormStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'field_type', 'form', 'form_step', 'field_order']

    def create(self, validated_data):
        label = "Untitled"

        field_type = validated_data['field_type']

        if field_type == FIELD_TYPES[1][0]:
            label = "Website"
        elif field_type == FIELD_TYPES[4][0]:
            label = "Email"
        elif field_type == FIELD_TYPES[16][0]:
            label = "Phone Number"

        validated_data['label'] = label

        return FormField.objects.create(**validated_data)


class ReOrderFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'field_order']


class UpdateFieldSettingsSerializer(serializers.ModelSerializer):
    def validate_validation_rule(self, value):
        if not value:
            raise serializers.ValidationError("Invalid Validation Rule")

        filed_type = self.instance.field_type
        # print(filed_type)

        schema = None

        if filed_type == FIELD_TYPES[0][0]:
            schema = get_text_box_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[1][0]:
            schema = get_website_url_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[2][0]:
            schema = get_textarea_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[3][0]:
            schema = get_number_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[4][0]:
            schema = get_email_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[5][0]:
            schema = get_dropdown_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[6][0]:
            schema = get_radio_field_validation_rule_schema()
        # elif filed_type == FIELD_TYPES[7][0]:
        #     schema = get_radio_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[8][0]:
            schema = get_date_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[9][0]:
            schema = get_time_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[10][0]:
            schema = get_file_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[11][0]:
            schema = get_short_textarea_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[12][0]:
            schema = get_multiselect_checkbox_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[13][0]:
            schema = get_hidden_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[16][0]:
            schema = get_phone_no_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[17][0]:
            schema = get_dynamic_dropdown_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[18][0]:
            schema = get_image_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[19][0]:
            schema = get_signature_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[20][0]:
            schema = get_location_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[21][0]:
            schema = get_unique_id_field_validation_rule_schema()

        if schema:
            try:
                validate(value, schema)
            except ValidationError as e:
                # print("Schema Error: ", e)
                raise serializers.ValidationError("Invalid Validation Rule")

            if filed_type == FIELD_TYPES[8][0]:
                # additional validation for date field
                if value['date']:
                    date_format = value['date_format']
                    field_rules_date_format_allowed = FIELD_RULES_DATE_FORMAT_ALLOWED.keys()
                    if date_format not in field_rules_date_format_allowed:
                        allowed_date_format = ", "
                        allowed_date_format = allowed_date_format.join(field_rules_date_format_allowed)
                        msg = f"Only {allowed_date_format} allowed for date format"
                        raise serializers.ValidationError(msg)
            elif filed_type == FIELD_TYPES[9][0]:
                # additional validation for time field
                if value['time']:
                    time_format = value['time_format']
                    field_rules_time_format_allowed = FIELD_RULES_TIME_FORMAT_ALLOWED.keys()
                    if time_format not in field_rules_time_format_allowed:
                        allowed_time_format = ", "
                        allowed_time_format = allowed_time_format.join(field_rules_time_format_allowed)
                        msg = f"Only {allowed_time_format} hrs allowed for time format"
                        raise serializers.ValidationError(msg)

        return value

    def validate_field_format(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank")

        # input_group_icon = []
        # if hasattr(settings, 'ZF_INPUT_GROUP_ICONS'):
        #     _input_group_icon = settings.ZF_INPUT_GROUP_ICONS
        #     if type(_input_group_icon) == list:
        #         input_group_icon = _input_group_icon

        schema = {
            "type": "object",
            "properties": {
                "field_format": {
                    "type": "string",
                    "enum": ["default", "input_group"]
                },
                "input_group_icon": {
                    "type": "string",
                },
                "input_group_icon_position": {
                    "type": "string",
                    "enum": ["start", "end"]
                },
            },
            "required": ["field_format"],
            "additionalProperties": False
        }

        try:
            validate(value, schema)
        except ValidationError as e:
            # print("Schema Error: ", e)
            raise serializers.ValidationError("Invalid Format")

        return value

    def validate_options(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank")

        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "value": {"type": "string"},
                    "label": {"type": "string"},
                    "order": {"type": "integer", "minimum": 0}
                },
                "required": ["value", "label", "order"],
                "additionalProperties": False
            }
        }

        try:
            validate(value, schema)
        except ValidationError as e:
            # print("Schema Error: ", e)
            raise serializers.ValidationError("Invalid Format")

        return value

    def validate_content(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank")

        return value

    def validate_content_size(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank")

        return value

    def validate_content_alignment(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank")

        allowed_content_alignment = ['left', 'center', 'right']

        if value not in allowed_content_alignment:
            allowed_content_alignment_msg = ", "
            allowed_content_alignment_msg = allowed_content_alignment_msg.join(allowed_content_alignment)
            raise serializers.ValidationError("Only " + allowed_content_alignment_msg + " allowed")

        return value

    def validate_label(self, value):
        try:
            unique_validation = settings.ZF_IS_FIELD_LABEL_UNIQUE
        except:
            unique_validation = True
        if unique_validation:
            is_duplicate = FormField.objects.filter(label=value, form__id=self.context.get('form_id')).exclude(
                id=self.context.get('field_id')).exclude(status=FORM_FIELD_STATUS[0][0]).exists()
            if is_duplicate:
                raise serializers.ValidationError("This field must be unique")
        return value

    def validate_slug(self, value):
        if value:
            is_duplicate = FormField.objects.filter(slug=value, form__id=self.context.get('form_id')).exclude(
                id=self.context.get('field_id')).exclude(status=FORM_FIELD_STATUS[0][0]).exists()
            if is_duplicate:
                raise serializers.ValidationError("This field must be unique")

        return value

    def validate(self, attrs):
        label_field = attrs.get('label', None)
        slug_field = attrs.get('slug', None)
        field_size_field = attrs.get('field_size', None)
        placeholder_field = attrs.get('placeholder', None)
        custom_class_name_field = attrs.get('custom_class_name', None)
        validation_rule_field = attrs.get('validation_rule', None)
        field_format_field = attrs.get('field_format', None)
        is_mandatory_field = attrs.get('is_mandatory', None)
        system_field = attrs.get('system_field', None)
        options_field = attrs.get('options', None)
        is_unique_field = attrs.get('is_unique', None)
        content_field = attrs.get('content', None)
        content_size_field = attrs.get('content_size', None)
        content_alignment_field = attrs.get('content_alignment', None)
        option_api_url = attrs.get('option_api_url', None)
        starts_from_field = attrs.get('starts_from', None)
        prefix_field = attrs.get('prefix', None)
        suffix_field = attrs.get('suffix', None)

        errors = {}

        field_type = self.instance.field_type

        if field_type != FIELD_TYPES[21][0]:
            if custom_class_name_field is None:
                errors["custom_class_name"] = ["This field is required"]
            if is_mandatory_field is None:
                errors["is_mandatory"] = ["This field is required"]

        if field_type != FIELD_TYPES[13][0] and field_type != FIELD_TYPES[21][0]:
            if field_size_field is None:
                errors["field_size"] = ["This field is required"]

        if field_type == FIELD_TYPES[0][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is None:
                errors["field_format"] = ["This field is required"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[1][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is None:
                errors["field_format"] = ["This field is required"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[2][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[3][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is None:
                errors["field_format"] = ["This field is required"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[4][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is None:
                errors["field_format"] = ["This field is required"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[5][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is None:
                errors["field_format"] = ["This field is required"]
            if options_field is None:
                errors["options"] = ["This field is required"]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[6][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is not None:
                errors["placeholder"] = ["Placeholder not allowed for this field type"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is None:
                errors["options"] = ["This field is required"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[7][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is not None:
                errors["placeholder"] = ["Placeholder not allowed for this field type"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is None:
                errors["options"] = ["This field is required"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[8][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[9][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[10][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[11][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[12][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is not None:
                errors["placeholder"] = ["Placeholder not allowed for this field type"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is None:
                errors["options"] = ["This field is required"]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[13][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is not None:
                errors["placeholder"] = ["Placeholder not allowed for this field type"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[14][0]:
            if label_field is not None:
                errors["label"] = ["Label not allowed for this field type"]
            if slug_field is not None:
                errors["slug"] = ["Slug not allowed for this field type"]
            if placeholder_field is not None:
                errors["placeholder"] = ["Placeholder not allowed for this field type"]
            if validation_rule_field is not None:
                errors["validation_rule"] = ["Validation Rule not allowed for this field type"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type"]
            if content_field is None:
                errors["content"] = ["This field is required"]
            if content_size_field is None:
                errors["content_size"] = ["This field is required"]
            if content_alignment_field is None:
                errors["content_alignment"] = ["This field is required"]

            allowed_content_size = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

            if content_size_field and content_size_field not in allowed_content_size:
                allowed_content_size_msg = ", "
                allowed_content_size_msg = allowed_content_size_msg.join(allowed_content_size)
                raise serializers.ValidationError("Only " + allowed_content_size_msg + " allowed")

        if field_type == FIELD_TYPES[15][0]:
            if label_field is not None:
                errors["label"] = ["Label not allowed for this field type"]
            if slug_field is not None:
                errors["slug"] = ["Slug not allowed for this field type"]
            if placeholder_field is not None:
                errors["placeholder"] = ["Placeholder not allowed for this field type"]
            if validation_rule_field is not None:
                errors["validation_rule"] = ["Validation Rule not allowed for this field type"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type"]
            if content_field is None:
                errors["content"] = ["This field is required"]
            if content_size_field is None:
                errors["content_size"] = ["This field is required"]
            if content_alignment_field is None:
                errors["content_alignment"] = ["This field is required"]

        if field_type == FIELD_TYPES[16][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is None:
                errors["field_format"] = ["This field is required"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[17][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is None:
                errors["field_format"] = ["This field is required"]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type"]
            if option_api_url is None or option_api_url == "":
                errors["option_api_url"] = ["This field is required"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[18][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if placeholder_field is None:
                errors["placeholder"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[19][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if slug_field is None:
                errors["slug"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[20][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if slug_field is None:
                errors["slug"] = ["This field is required"]
            if validation_rule_field is None:
                errors["validation_rule"] = ["This field is required"]
            if field_format_field is not None:
                errors["field_format"] = ["Field Format not allowed for this field type"]
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type"]
            if content_field is not None:
                errors["content"] = ["Content not allowed for this field type"]
            if content_size_field is not None:
                errors["content_size"] = ["Content Size not allowed for this field type"]
            if content_alignment_field is not None:
                errors["content_alignment"] = ["Content Alignment not allowed for this field type"]

        if field_type == FIELD_TYPES[21][0]:
            if label_field is None:
                errors["label"] = ["This field is required"]
            if starts_from_field is None:
                errors["starts_from"] = ["This field is required"]

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    options = serializers.JSONField(required=False)

    class Meta:
        model = FormField
        fields = ['id', 'label', 'field_size', 'placeholder', 'custom_class_name', 'validation_rule', 'is_mandatory',
                  'system_field', 'admin_only_edit', 'admin_can_submit', 'user_can_submit', 'is_unique', 'options',
                  'field_format', 'content', 'content_size', 'content_alignment','slug','option_api_url', 'starts_from',
                  'prefix','suffix']
        extra_kwargs = {
            "label": {"required": False},
            "slug": {"required": False},
            "field_size": {"required": False},
            "placeholder": {"required": False, "allow_blank": True},
            "custom_class_name": {"required": False},
            "validation_rule": {"required": False},
            "is_mandatory": {"required": False},
            "is_unique": {"required": False},
        }


class FormPaymentSettingsSerializer(serializers.ModelSerializer):
    def validate(self, value):
        payment_mode = value.get('payment_mode', '')
        payment_type = value.get('payment_type', '')
        currency = value.get('currency', '')
        price = value.get('price', '')
        redirect_url = value.get('redirect_url', '')
        dynamic_price_field = value.get('dynamic_price_field', None)
        payment_gateway = value.get('payment_gateway', '')
        tax_enabled = value.get('tax_enabled', False)
        tax_display_name = value.get('tax_display_name', '')
        tax = value.get('tax', '')

        boolean_fields = [True, False]

        error = {}

        if not payment_type:
            error['payment_type'] = ['This field is required']
        if not payment_gateway:
            error['payment_gateway'] = ['This field is required']
        if not payment_mode:
            error['payment_mode'] = ['This field is required']
        if not currency:
            error['currency'] = ['This field is required']
        if not redirect_url:
            error['redirect_url'] = ['This field is required']
        if tax_enabled not in boolean_fields:
            error['tax_enable'] = ['This field is required']
        elif tax_enabled:
            if not tax_display_name:
                error['tax_display_name'] = ['This field is required']
            if not tax:
                error['tax'] = ['This field is required']
            try:
                float(tax)
                if float(tax) == float(0):
                    error['tax'] = ['Invalid Tax']
            except:
                error['tax'] = ['Invalid Tax']

        if payment_type:
            if payment_type == PAYMENT_TYPE[0][0]:
                if not price:
                    error['price'] = ['This field is required']
                elif "." in price:
                    error['price'] = ['Decimal value not allowed']
                # if dynamic_price_field:
                #     error['dynamic_price_field'] = ['Dynamic Price Field not allowed']
            elif payment_type == PAYMENT_TYPE[1][0]:
                if price:
                    error['price'] = ['Price Field not allowed']
                # if not dynamic_price_field:
                #     error['dynamic_price_field'] = ['This field is required']

        if payment_gateway:
            payment_gateway_value = False
            for payment_gateways in PAYMENT_GATEWAYS:
                if payment_gateway == payment_gateways[0]:
                    payment_gateway_value = True
                    break

            if not payment_gateway_value:
                error['payment_gateway'] = ['Invalid Payment Gateway']

        if dynamic_price_field:
            dynamic_field = FormField.objects.filter(id=dynamic_price_field.id).filter(field_type=FIELD_TYPES[3][0],
                                                                                       status=FORM_FIELD_STATUS[1][
                                                                                           0]).first()
            if dynamic_field:
                validation_rule = dynamic_field.validation_rule['required']
                if validation_rule == False:
                    error['dynamic_price_field'] = [
                        "The selected field for capturing the price must be mandatory. Please ensure it is marked as required to proceed"]
            else:
                error['dynamic_price_field'] = ["Invalid Field"]

        if error != {}:
            raise serializers.ValidationError(error)
        return value

    class Meta:
        model = FormPaymentSettings
        fields = ['id', 'payment_type', 'payment_mode', 'currency', 'price', 'tax_enabled', 'tax', 'tax_display_name',
                  'form', 'account', 'redirect_url',
                  'dynamic_price_field', 'payment_gateway']


class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = ['id', 'endpoint_url', 'description', 'event_new_form_created', 'event_form_submit', 'account',
                  'status']

    def validate(self, attrs):
        endpoint_url = attrs.get('endpoint_url', None)
        description = attrs.get('description', None)
        event_form_submit = attrs.get('event_form_submit', False)
        account = attrs.get('account', '')
        forms = self.context.get('forms', [])

        errors = {}

        if endpoint_url is None:
            errors['endpoint_url'] = ["This field is required"]

        if event_form_submit:
            if not forms:
                errors["forms"] = ['This field is required']
            else:
                invalid_forms = []
                for form_id in forms:
                    try:
                        Form.objects.filter(id=form_id, account_id=account, status=FORM_STATUS[1][0]).get()
                    except:
                        invalid_forms.append(form_id)
                if invalid_forms:
                    errors["forms"] = "Only active forms allowed"
                    errors["invalid_forms"] = invalid_forms
        else:
            if forms:
                errors["forms"] = "Forms allowed only if form submit event enabled"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
