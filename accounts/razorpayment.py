import razorpay

client = razorpay.Client(auth=("rzp_test_Ar1T5bGrLxxKsY", "QrSylQtocQeSOStbuj7vmX2i"))
client.set_app_details({"title": "Buidcron", "version": "1.0"})

# response = client.order.create({'amount':50000,'currency':'INR','payment_capture':1})
# print(response)

def get_payments(payment_id=None):
    if payment_id:
        return client.payment.fetch(payment_id)
    else:
        return client.payment.all()


def capture_payment(payment_id, amount):
    return client.payment.capture(payment_id, amount)


def refund_payment(payment_id, amount):
    return client.payment.refund(payment_id, amount)


def get_bank_transefer_details(payment_id):
    return client.payment.bank_transfer(payment_id)


def get_payments(refund_id=None):
    if refund_id:
        return client.refund.fetch(refund_id)
    else:
        return client.payment.all()


def create_payment_link(data=None):
    # data = {
    #     "customer": {
    #         "name": "Test Customer",
    #         "email": "test@example.com",
    #         "contact": "+919999888877"
    #     },
    #     "type": "link",
    #     "amount": 100,
    #     "currency": "INR",
    #     "description": "Payment link for this purpose - xyz",
    #     "callback_url": 'https://your-server/callback_url',
    #     "callback_method": "get"
    # }
    return client.invoice.create(data=data)


def fetch_payment_link(invoice_id=None):
    if invoice_id:
        return client.invoice.fetch(invoice_id)
    else:
        client.invoice.all()


def cancel_payment_link(invoice_id):
    return client.invoice.cancel(invoice_id)


def send_notification(invoice_id, medium):
    return client.invoice.notify_by(invoice_id, medium)


def edit_invoice(invoice_id, DATA):
    return client.invoice.edit(invoice_id=invoice_id, data=DATA)


def fetch_customer_info(customer_id):
    return client.customer.fetch(customer_id=customer_id)


def create_customer(data):
    return client.customer.create(data=data)


def edit_customer(customer_id, data):
    return client.customer.edit(customer_id=customer_id, data=data)