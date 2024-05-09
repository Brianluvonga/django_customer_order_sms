from django import forms
from .models import Customer, Order
import random
from django.core.validators import RegexValidator


def generate_unique_code():
    return str(random.randint(100000, 999999))


class PhoneNumberField(forms.CharField):
    default_validators = [RegexValidator(r"^\+254\d{9}$")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial = "+254"  # Set the initial value to '+254'

    def clean(self, value):
        value = super().clean(value)
        if value and not value.startswith("+254"):
            value = "+254" + value
        return value


class CustomerForm(forms.ModelForm):
    phone_number = PhoneNumberField()

    class Meta:
        model = Customer
        fields = ["name", "phone_number"]  # Exclude 'code' field from the form

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Generate a unique code here
        instance.code = generate_unique_code()
        if commit:
            instance.save()
        return instance


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "item", "amount"]
