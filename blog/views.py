from django.shortcuts import render
from .models import Post

def Posts(request):
    posts = Post.objects.all()
    context = {
        'posts_list': posts,
    }
    return render(request, 'blog/posts.html', context)