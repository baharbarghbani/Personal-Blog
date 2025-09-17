from django.shortcuts import render
from .models import Post
from .forms import CommentForm

def Posts(request):
    posts = Post.objects.all()
    context = {
        'posts_list': posts,
    }
    return render(request, 'blog/posts.html', context)

def PostDetail(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {
        "post": post,
        "form": CommentForm,
    }
    return render(request, "blog/post_detail.html", context)
