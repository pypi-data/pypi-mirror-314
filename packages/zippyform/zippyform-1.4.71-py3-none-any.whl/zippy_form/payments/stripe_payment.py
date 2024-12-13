import stripe

from zippy_form.utils import PAYMENT_TYPE, APPLICATION_TYPE


def stripe_create_product(secret_key, application_type, connected_account_id, name):
    """
    Create Product in Stripe
    """
    stripe.api_key = secret_key

    if application_type == APPLICATION_TYPE[1][0]:
        created_product = stripe.Product.create(name=name, stripe_account=connected_account_id)
    else:
        created_product = stripe.Product.create(name=name)

    return created_product.id


def stripe_update_product(secret_key, application_type, connected_account_id, product_id, name):
    """
    Update Stripe Product
    """
    stripe.api_key = secret_key

    if application_type == APPLICATION_TYPE[1][0]:
        stripe.Product.modify(product_id, name=name, stripe_account=connected_account_id)
    else:
        stripe.Product.modify(product_id, name=name)


def stripe_create_price(secret_key, application_type, connected_account_id, product_id, payment_type, currency, amount):
    """
    Create Price for Stripe Product
    """
    stripe.api_key = secret_key

    if payment_type == PAYMENT_TYPE[0][0]:
        # Handle For Fixed Price
        unit_amount = int(float(amount) * 100)
        if application_type == APPLICATION_TYPE[1][0]:
            created_price = stripe.Price.create(currency=currency, unit_amount=unit_amount, product=product_id,
                                                stripe_account=connected_account_id)
        else:
            created_price = stripe.Price.create(currency=currency, unit_amount=unit_amount, product=product_id)
    else:
        # Handle For Dynamic Price
        preset_amount = 500 * 10  # 50
        if application_type == APPLICATION_TYPE[1][0]:
            created_price = stripe.Price.create(currency=currency,
                                                custom_unit_amount={"enabled": True, "preset": preset_amount},
                                                product=product_id,
                                                stripe_account=connected_account_id)
        else:
            created_price = stripe.Price.create(currency=currency,
                                                custom_unit_amount={"enabled": True, "preset": preset_amount},
                                                product=product_id)

    return created_price.id


def stripe_update_price(secret_key, application_type, connected_account_id, product_id, payment_type, currency, amount,
                        price_id):
    """
    Update Stripe Product Price
    """
    stripe.api_key = secret_key

    if application_type == APPLICATION_TYPE[1][0]:
        # InActivate Existing Stripe Price
        stripe.Price.modify(price_id, active=False, stripe_account=connected_account_id)
    else:
        # InActivate Existing Stripe Price
        stripe.Price.modify(price_id, active=False)

    # Create New Price For The Product
    created_price_id = stripe_create_price(secret_key, application_type, connected_account_id, product_id,
                                           payment_type,
                                           currency, amount)

    return created_price_id


def stripe_create_tax(secret_key, application_type, connected_account_id, tax_display_name,
                      tax_percentage):
    """
    Create Tax Rate
    """
    stripe.api_key = secret_key

    tax_percentage = float(tax_percentage)
    if application_type == APPLICATION_TYPE[1][0]:
        created_tax = stripe.TaxRate.create(display_name=tax_display_name, percentage=tax_percentage,
                                            inclusive=False, stripe_account=connected_account_id)
    else:
        created_tax = stripe.TaxRate.create(display_name=tax_display_name, percentage=tax_percentage,
                                            inclusive=False)

    return created_tax.id


def stripe_update_tax(secret_key, application_type, connected_account_id, tax_display_name,
                      tax_percentage, tax_id):
    """
    Update Stripe Tax Rate
    """
    stripe.api_key = secret_key

    if application_type == APPLICATION_TYPE[1][0]:
        # InActivate Existing Stripe Tax
        stripe.TaxRate.modify(tax_id, active=False, stripe_account=connected_account_id)
    else:
        # InActivate Existing Stripe Tax
        stripe.TaxRate.modify(tax_id, active=False)

    # Create New Tax Rate
    created_tax_id = stripe_create_tax(secret_key, application_type, connected_account_id,
                                       tax_display_name, tax_percentage)

    return created_tax_id


def stripe_create_checkout(secret_key, application_type, connected_account_id, payment_type, application_fee_amount,
                           line_items, after_payment_redirect_url, form_id, form_submission_id,
                           form_submission_payment_detail_id):
    """
    Create Stripe Checkout - Checkout Session
    """
    stripe.api_key = secret_key

    application_fee_amount = int(float(application_fee_amount) * 100)

    stripe.api_key = secret_key

    if application_type == APPLICATION_TYPE[1][0]:
        # Handle for SaaS Application
        try:
            session = stripe.checkout.Session.create(
                ui_mode='embedded',
                mode='payment',
                line_items=line_items,
                payment_intent_data={
                    'application_fee_amount': application_fee_amount,
                },
                stripe_account=connected_account_id,
                return_url=after_payment_redirect_url,
                metadata={'form_id': form_id, 'form_submission_id': form_submission_id,
                          'form_submission_payment_detail_id': form_submission_payment_detail_id,
                          'application': "ZippyFormApplication"
                          }
            )
        except Exception as e:
            session = {"error": str(e), "client_secret": ""}
    else:
        # Handle for Standalone Application
        try:
            session = stripe.checkout.Session.create(
                ui_mode='embedded',
                mode='payment',
                line_items=line_items,
                return_url=after_payment_redirect_url,
                metadata={'form_id': form_id, 'form_submission_id': form_submission_id,
                          'form_submission_payment_detail_id': form_submission_payment_detail_id,
                          'application': "ZippyFormApplication"
                          }
            )
        except Exception as e:
            session = {"error": str(e), "client_secret": ""}

    return session


def stripe_create_checkout2(secret_key, application_type, connected_account_id, payment_type, application_fee_amount,
                            line_items, after_payment_redirect_url, form_id):
    """
    Create Stripe Checkout - Payment Intent
    """
    stripe.api_key = secret_key

    application_fee_amount = int(float(application_fee_amount) * 100)

    stripe.api_key = secret_key

    if application_type == APPLICATION_TYPE[1][0]:
        # Handle for SaaS Application
        try:
            session = stripe.PaymentIntent.create(
                amount=line_items["unit_amount"],
                currency=line_items["currency"],
                automatic_payment_methods={"enabled": True},
                stripe_account=connected_account_id,
                metadata={'form_id': form_id}
            )
        except Exception as e:
            session = {"error": str(e), "client_secret": ""}
    else:
        # Handle for Standalone Application
        try:
            session = stripe.PaymentIntent.create(
                amount=line_items["unit_amount"],
                currency=line_items["currency"],
                automatic_payment_methods={"enabled": True},
                metadata={'form_id': form_id}
            )
        except Exception as e:
            session = {"error": str(e), "client_secret": ""}

    return session


def stripe_connect(secret_key, code):
    """
    Stripe Connect
    """
    stripe.api_key = secret_key

    try:
        response = stripe.OAuth.token(
            grant_type='authorization_code',
            code=code
        )
    except Exception as e:
        response = {
            "error": str(e),
            "stripe_user_id": ""
        }

    return response


def stripe_create_webhook(secret_key, application_type, webhook_url):
    """
    Create Webhook
    """
    stripe.api_key = secret_key

    if application_type == APPLICATION_TYPE[1][0]:
        webhook = stripe.WebhookEndpoint.create(
            url=webhook_url,
            enabled_events=["checkout.session.completed"],
            connect=True,
        )
    else:
        webhook = stripe.WebhookEndpoint.create(
            url=webhook_url,
            enabled_events=["checkout.session.completed"],
        )

    return webhook.id


def stripe_list_webhook(secret_key, application_type):
    """
    List Webhook
    """
    stripe.api_key = secret_key

    webhooks = stripe.WebhookEndpoint.list()

    return webhooks
