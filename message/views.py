import json
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout as django_logout
from decouple import config
from .forms import CustomerForm, OrderForm
from .models import Customer, Order
from .sms import send_sms


from django.http import HttpResponseRedirect

# display home screen
def home(request):
    return render(request, "index.html")

# view logged in user information
def profileSection(request):
    user = request.user
    if user.is_authenticated:
        auth0_user = user.social_auth.get(provider="auth0")
        extra_data = auth0_user.extra_data
        first_name = extra_data.get("name", "")

        data = {
            "id": auth0_user.uid,
            "username": first_name,
            "picture": extra_data.get("picture", ""),
        }
        context = {"user_data": json.dumps(data, indent=4), "auth0_user": auth0_user}
        return render(request, "profile.html", context)
    else:
        # case when the user is not authenticated
        return redirect("index.html")

# logout user and redirect
def logout(request):
    django_logout(request)

    domain = config("APP_DOMAIN")
    client_id = config("APP_CLIENT_ID")
    return_to = "http://localhost:8000/"

    return HttpResponseRedirect(
        f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}"
    )


# orders and customers entries section

# view customer entries
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "customer_list.html", {"customers": customers})

# view customer details
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "customer_detail.html", {"customer": customer})

# view order entries
def order_list(request):
    orders = Order.objects.all()
    return render(request, "order_list.html", {"orders": orders})

# create and save a customer
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
    else:
        form = CustomerForm()
    return render(request, "customer_form.html", {"form": form})

# book an order and send sms
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            customer = order.customer
            send_sms(customer, order)  # Send SMS alert
            return redirect("order_list")
    else:
        form = OrderForm()
    return render(request, "order_form.html", {"form": form})

