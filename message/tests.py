from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from .sms import send_sms


# view test
class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.customer = Customer.objects.create(
            name="Test Customer", code="TC001", phone_number="+254712345678"
        )
        self.order = Order.objects.create(
            customer=self.customer, item="Test Item", amount=100
        )

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_customer_list_view(self):
        response = self.client.get(reverse("customer_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customer_list.html")
        self.assertContains(response, self.customer.name)

    def test_customer_detail_view(self):
        response = self.client.get(reverse("customer_detail", args=[self.customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customer_detail.html")
        self.assertContains(response, self.customer.name)

    def test_order_list_view(self):
        response = self.client.get(reverse("order_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order_list.html")
        self.assertContains(response, self.order.item)

    def test_profile_section_unauthenticated(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)  # Redirect to login page

    @patch("message.views.django_logout")
    def test_logout_view(self, mock_logout):
        self.client.force_login(self.user)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        mock_logout.assert_called_once()

    def test_customer_create_get(self):
        response = self.client.get(reverse("customer_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customer_form.html")

    def test_customer_create_post(self):
        data = {
            "name": "New Customer",
            "code": "NC001",
            "phone_number": "+254987654321",
        }
        response = self.client.post(reverse("customer_create"), data)
        self.assertEqual(response.status_code, 302)  # Redirect to customer_list
        self.assertTrue(Customer.objects.filter(name="New Customer").exists())



# model tests
class ModelTestCase(TestCase):
    def test_customer_model(self):
        customer = Customer.objects.create(
            name="Test Customer", code="TC001", phone_number="+254712345678"
        )
        self.assertEqual(str(customer), "Test Customer")
        self.assertEqual(customer.phone_number, "+254712345678")

    def test_order_model(self):
        customer = Customer.objects.create(
            name="Test Customer", code="TC001", phone_number="+254712345678"
        )
        order = Order.objects.create(customer=customer, item="Test Item", amount=100)
        self.assertEqual(str(order), "Test Item (x100) - Test Customer")
        self.assertEqual(order.customer.name, "Test Customer")


# serializers test
class SerializerTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer", code="TC001", phone_number="+254712345678"
        )
        self.order = Order.objects.create(
            customer=self.customer, item="Test Item", amount=100
        )

    def test_customer_serializer(self):
        serializer = CustomerSerializer(instance=self.customer)
        data = serializer.data

        self.assertEqual(data["name"], "Test Customer")
        self.assertEqual(data["code"], "TC001")
        self.assertEqual(data["phone_number"], "+254712345678")

    def test_order_serializer(self):
        serializer = OrderSerializer(instance=self.order)
        data = serializer.data

        self.assertEqual(data["customer"], self.customer.pk)
        self.assertEqual(data["item"], "Test Item")
        self.assertEqual(data["amount"], 100)


# sms tests


class SMSTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer", code="TC001", phone_number="+254712345678"
        )
        self.order = Order.objects.create(
            customer=self.customer, item="Test Item", amount=100
        )

    @patch("africastalking.SMS.send")
    def test_send_sms(self, mock_send):
        send_sms(self.customer, self.order)

        expected_message = (
            f"New order placed: {self.order.item} (Ksh.{str(self.order.amount)})"
        )
        expected_recipient = [self.customer.phone_number]

        mock_send.assert_called_once_with(expected_message, expected_recipient)

    # @patch('africastalking.SMS.send')
    # def test_send_sms_error(self, mock_send):
    #     mock_send.side_effect = Exception("Test exception")

    #     with self.assertLogs('root', level='ERROR') as cm:
    #         send_sms(self.customer, self.order)

    #     self.assertIn("Error sending SMS: Test exception", cm.output)

    # def test_send_sms_empty_order(self):
    #     order = Order.objects.create(customer=self.customer, item="", amount=0)

    #     with self.assertLogs('root', level='ERROR') as cm:
    #         send_sms(self.customer, order)

    #     self.assertIn("Error sending SMS: Invalid order details", cm.output)

    # def test_send_sms_invalid_phone_number(self):
    #     customer = Customer.objects.create(
    #         name="Test Customer", code="TC002", phone_number="invalid"
    #     )
    #     order = Order.objects.create(customer=customer, item="Test Item", amount=100)

    #     with self.assertLogs('root', level='ERROR') as cm:
    #         send_sms(customer, order)

    #     self.assertIn("Error sending SMS: Invalid phone number", cm.output)
