import requests

from zippy_form.models import Webhook, WebhookForm
from zippy_form.utils import WEBHOOK_STATUS


def get_webhooks_using_account(event, account_id):
    """
    Get Webhooks Using User Account
    """
    if event == 'form.created':
        user_account_webhooks = Webhook.objects.filter(account=account_id, event_new_form_created=True,
                                                       status=WEBHOOK_STATUS[1][0])

    webhook_urls = []

    # Get User Account Webhooks
    for user_account_webhook in user_account_webhooks:
        temp = {'webhook_id': user_account_webhook.id, 'endpoint_url': user_account_webhook.endpoint_url}

        webhook_urls.append(temp)

    return webhook_urls


def get_webhooks_using_form(event, form_id):
    """
    Get Webhooks Using From ID
    """
    if event == 'form.submit':
        user_account_form_webhooks = WebhookForm.objects.filter(form=form_id, event_form_submit=True, webhook__status=WEBHOOK_STATUS[1][0])

    webhook_urls = []
    for user_account_form_webhook in user_account_form_webhooks:
        temp = {'webhook_id': user_account_form_webhook.webhook.id, 'endpoint_url': user_account_form_webhook.webhook.endpoint_url}

        webhook_urls.append(temp)

    return webhook_urls


try:
    from celery_init import app
except ImportError:
    from zippy_form.celery import app


@app.task
def handle_webhook_queue(data):
    """
    Handle Webhook Queue
    """
    account_id = data['account']['id']
    form_id = data['form']['id']
    event = data['event']

    if event == 'form.created':
        webhooks = get_webhooks_using_account(event, account_id)
    elif event == 'form.submit':
        webhooks = get_webhooks_using_form(event, form_id)

    webhook_response = []

    # Loop all the Webhooks & send event data to the URL provided by user
    for webhook in webhooks:
        response = {}

        try:
            webhook_info = requests.post(webhook['endpoint_url'], json=data)
            response['status'] = "success"
            response['status_code'] = webhook_info.status_code
            response['webhook'] = {}
            response['webhook']['id'] = str(webhook['webhook_id'])
            response['webhook']['url'] = str(webhook['endpoint_url'])
            response['account_id'] = account_id
        except Exception as e:
            response['status'] = "error"
            response['webhook'] = {}
            response['webhook']['id'] = str(webhook['webhook_id'])
            response['webhook']['url'] = str(webhook['endpoint_url'])
            response['account_id'] = account_id
            response['data'] = str(e)

        webhook_response.append(response)

    return webhook_response
