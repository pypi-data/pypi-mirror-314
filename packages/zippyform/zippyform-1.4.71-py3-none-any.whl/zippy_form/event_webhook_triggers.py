from django.conf import settings

from zippy_form.celery_tasks import handle_webhook_queue


def handle_webhook(data):
    """
    Handle Webhook
    """
    try:
        # Webhook Settings Added
        is_webhook_enabled = settings.ZF_ENABLE_WEBHOOK
        broker_url = settings.ZF_WEBHOOK_BROKER_URL
        backend = settings.ZF_WEBHOOK_BACKEND

        if is_webhook_enabled and broker_url and backend:
            webhook_response = handle_webhook_queue.delay(data)

            # try:
            #     print("Webhook Response: ", webhook_response.get())
            # except:
            #     print("Webhook Response: Error")
    except:
        # Webhook Settings Not Added
        pass


def after_account_create(data):
    """
    After Account Create Event
    """
    # Event
    if hasattr(settings, 'ZF_EVENT_AFTER_ACCOUNT_CREATE'):
        try:
            # Event Callback Function Provided In Project Settings File
            settings.ZF_EVENT_AFTER_ACCOUNT_CREATE(data)
        except:
            print("Event Callback Error: Invalid Callback Function")


def after_form_create(data):
    """
    After Form Create Event & Webhook
    """
    # Event
    if hasattr(settings, 'ZF_EVENT_AFTER_FORM_CREATE'):
        try:
            # Event Callback Function Provided In Project Settings File
            settings.ZF_EVENT_AFTER_FORM_CREATE(data)
        except:
            print("Event Callback Error: Invalid Callback Function")

    # Webhook
    handle_webhook(data)


def after_form_submit(data):
    """
    After Form Submit Event & Webhook
    """
    # Event
    if hasattr(settings, 'ZF_EVENT_AFTER_FORM_SUBMIT'):
        try:
            # Event Callback Function Provided In Project Settings File
            settings.ZF_EVENT_AFTER_FORM_SUBMIT(data)
        except:
            print("Event Callback Error: Invalid Callback Function")

    # Webhook
    handle_webhook(data)