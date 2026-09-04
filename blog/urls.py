from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path("posts/", views.posts, name="posts"),
    path("posts/<int:post_id>/", views.legacy_post_detail, name="legacy-detail"),
    path("posts/<str:slug>/", views.post_detail, name="detail"),
    path("comments/<int:comment_id>/edit/", views.edit_comment, name="comment-edit"),
    path(
        "comments/<int:comment_id>/delete/",
        views.delete_comment,
        name="comment-delete",
    ),
] 
