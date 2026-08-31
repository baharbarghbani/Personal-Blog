from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentForm
from .models import Post


def posts(request):
    posts = Post.objects.published()
    context = {
        "posts_list": posts,
    }
    return render(request, "blog/posts.html", context)


def legacy_post_detail(request, post_id):
    posts = Post.objects.all() if request.user.is_staff else Post.objects.published()
    post = get_object_or_404(posts, pk=post_id)

    if request.method == "POST":
        return post_detail(request, slug=post.slug)

    return redirect(post, permanent=True)


def post_detail(request, slug):
    posts = Post.objects.all() if request.user.is_staff else Post.objects.published()
    post = get_object_or_404(posts, slug=slug)

    if request.method == "POST" and not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path(), reverse("login"))

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            display_name = request.user.get_full_name() or request.user.username
            name_max_length = comment._meta.get_field("name").max_length
            comment.name = display_name[:name_max_length]
            comment.save()
            messages.success(request, "Your comment has been added.")
            return redirect(post)
    else:
        form = CommentForm()

    context = {
        "post": post,
        "form": form,
    }
    return render(request, "blog/post_detail.html", context)
