from django.urls import path, include
from . import views



urlpatterns = [
    # authentication section
    path("", views.home, name="home"),
    path("profile/", views.profileSection, name="profile"),
    path("", include("social_django.urls")),
    path("logout/", views.logout, name="logout"),
    # create and sms section
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/<int:pk>/", views.customer_detail, name="customer_detail"),
    path("orders/", views.order_list, name="order_list"),
    path("customers/create/", views.customer_create, name="customer_create"),
    path("orders/create/", views.order_create, name="order_create"),
]
