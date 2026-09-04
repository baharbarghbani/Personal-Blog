from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CommentForm
from .models import Comment, Post


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

    if request.method == "POST":
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author = request.user
                display_name = request.user.get_full_name() or request.user.username
                name_max_length = comment._meta.get_field("name").max_length
                comment.name = display_name[:name_max_length]
            else:
                comment.name = form.cleaned_data.get("name") or "Anonymous"
            comment.save()
            messages.success(request, "Your comment has been published.")
            return redirect(post)
    else:
        form = CommentForm(user=request.user)

    context = {
        "post": post,
        "form": form,
        "comments": post.comments.select_related("author"),
    }
    return render(request, "blog/post_detail.html", context)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(
        Comment.objects.select_related("post"),
        pk=comment_id,
        author=request.user,
    )

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment, user=request.user)
        if form.is_valid():
            edited_comment = form.save(commit=False)
            edited_comment.edited_at = timezone.now()
            edited_comment.save()
            messages.success(request, "Your comment has been updated.")
            return redirect(comment.post)
    else:
        form = CommentForm(instance=comment, user=request.user)

    return render(
        request,
        "blog/comment_edit.html",
        {"comment": comment, "form": form},
    )


@login_required
@require_POST
def delete_comment(request, comment_id):
    comments = Comment.objects.select_related("post")
    if not request.user.is_staff:
        comments = comments.filter(author=request.user)

    comment = get_object_or_404(comments, pk=comment_id)
    post = comment.post
    comment.delete()
    messages.success(request, "The comment has been deleted.")
    return redirect(post)
