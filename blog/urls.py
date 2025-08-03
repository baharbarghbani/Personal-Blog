from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path("posts/", views.Posts, name="posts"),
    path("posts/<int:post_id>/", views.PostDetail, name="detail"),
] 
