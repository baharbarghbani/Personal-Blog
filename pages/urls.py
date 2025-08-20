from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path("home/", views.HomePage, name='home'),
    path("about/", views.About, name='about'),
    path("contact/", views.Contact, name='contact'),
    path("thank_you/", views.Thankyou, name='thank-you'),
]