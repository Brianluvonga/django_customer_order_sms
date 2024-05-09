from django.db import models
from django.core.validators import RegexValidator



class PhoneNumberField(models.CharField):
    default_validators = [RegexValidator(r'^\+254\d{9}$')]

    def to_python(self, value):
        if isinstance(value, str):
            if not value.startswith('+254'):
                value = '+254' + value
        return super().to_python(value)

    def from_db_value(self, value, expression, connection):
        if value is not None:
            if not value.startswith('+254'):
                value = '+254' + value
        return value
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    phone_number = PhoneNumberField(max_length=13)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    item = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} (x{self.amount}) - {self.customer.name}"
