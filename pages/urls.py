from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path("", views.HomePage, name='home'),
    path("about/", views.About, name='about'),
]