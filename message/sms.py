import africastalking

username = "appname"
api_key = "your-api key"

africastalking.initialize(username, api_key)
sms = africastalking.SMS


def send_sms(customer, order):
    message = f"New order placed: {order.item} (Ksh.{str(order.amount)})"
    recipient = [
        customer.phone_number
    ]  # Use the customer phone number as the recipient

    try:
        response = sms.send(message, recipient)
        print(response)
    except Exception as e:
        print(f"Error sending SMS: {e}")

