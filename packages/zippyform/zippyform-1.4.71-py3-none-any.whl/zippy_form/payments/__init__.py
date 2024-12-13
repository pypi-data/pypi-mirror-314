from zippy_form.utils import PAYMENT_GATEWAYS
from zippy_form.payments.stripe_payment import stripe_create_product, stripe_update_product, stripe_create_price, \
    stripe_update_price, \
    stripe_create_checkout, stripe_create_webhook, stripe_list_webhook, stripe_create_tax, stripe_update_tax


class Payment:
    def __init__(self, primary_payment_gateway, secret_key, application_type, connected_account_id=""):
        self.primary_payment_gateway = primary_payment_gateway
        self.secret_key = secret_key
        self.application_type = application_type
        self.connected_account_id = connected_account_id

    def create_product(self, name):
        """
        Create Product
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            created_product = stripe_create_product(self.secret_key, self.application_type, self.connected_account_id,
                                                    name)

            return created_product

    def update_product(self, product_id, name):
        """
        Update Product
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            stripe_update_product(self.secret_key, self.application_type, self.connected_account_id, product_id, name)

    def create_price(self, product_id, payment_type, currency, amount):
        """
        Create Price
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            created_price = stripe_create_price(self.secret_key, self.application_type, self.connected_account_id,
                                                product_id,
                                                payment_type, currency, amount)

            return created_price

    def update_price(self, product_id, payment_type, currency, amount, price_id):
        """
        Update Price
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            updated_price = stripe_update_price(self.secret_key, self.application_type, self.connected_account_id,
                                                product_id, payment_type,
                                                currency, amount, price_id)

            return updated_price

    def create_tax(self, tax_display_name, tax_percentage):
        """
        Create Tax
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            created_tax = stripe_create_tax(self.secret_key, self.application_type, self.connected_account_id,
                                            tax_display_name, tax_percentage)

            return created_tax

    def update_tax(self, tax_display_name, tax_percentage, tax_id):
        """
        Update Tax
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            updated_tax = stripe_update_tax(self.secret_key, self.application_type, self.connected_account_id,
                                            tax_display_name, tax_percentage, tax_id)

            return updated_tax

    def checkout(self, payment_type, application_fee_amount, line_items, after_payment_redirect_url, form_id, form_submission_id, form_submission_payment_detail_id):
        """
        Checkout
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            session = stripe_create_checkout(self.secret_key, self.application_type,
                                                            self.connected_account_id, payment_type,
                                                            application_fee_amount,
                                                            line_items, after_payment_redirect_url, form_id, form_submission_id, form_submission_payment_detail_id)

            return session

    def create_webhook(self, webhook_url):
        """
        Create Webhook
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            created_webhook = stripe_create_webhook(self.secret_key, self.application_type, webhook_url)

            return created_webhook

    def list_webhook(self):
        """
        List Webhook
        """
        if self.primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
            webhooks = stripe_list_webhook(self.secret_key, self.application_type)

            return webhooks


"""
Usage Example:

payment = Payment("stripe", "YourSecretKey", "saas", "")
create_product_id = payment.create_product("Test Form")
"""
