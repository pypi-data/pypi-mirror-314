from celery import Celery
from django.conf import settings

app = Celery('zippy_form', include=['zippy_form.celery_tasks'])

try:
    is_webhook_enabled = settings.ZF_ENABLE_WEBHOOK
    broker_url = settings.ZF_WEBHOOK_BROKER_URL
    backend = settings.ZF_WEBHOOK_BACKEND

    if is_webhook_enabled:
        # if webhook enabled
        app.conf.broker_url = broker_url
        app.conf.result_backend = backend

        app.conf.broker_connection_retry_on_startup = True
        app.autodiscover_tasks()
    else:
        print("Error: Set ZF_ENABLE_WEBHOOK=True in your_project.settings.py to enable Webhook.")
except:
    print("Error: ZF_ENABLE_WEBHOOK or ZF_WEBHOOK_BROKER_URL or ZF_WEBHOOK_BACKEND missing in your_project.settings.py")


