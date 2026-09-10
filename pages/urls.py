from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path("", views.HomePage, name='home'),
    path("about/", views.About, name='about'),
    path("research/", views.research, name="research"),
    path("research/<str:slug>/", views.research_detail, name="research-detail"),
    path("projects/", views.projects, name="projects"),
    path("projects/<str:slug>/", views.project_detail, name="project-detail"),
    path("experience/", views.experience, name="experience"),
    path("cv/", views.download_cv, name="cv-download"),
    path("contact/", views.Contact, name='contact'),
    path("thank_you/", views.Thankyou, name='thank-you'),
]
