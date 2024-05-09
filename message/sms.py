import africastalking

username = "insane"
api_key = "b4b9800271468190e1c156195e83aa2c0b570aad329a1d105ecebf3a1099e634"

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

