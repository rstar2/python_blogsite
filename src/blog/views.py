from django.shortcuts import render, get_object_or_404
from .models import Post


# Create your views here.

def post_list(request):
    posts = Post.status_published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, status='posted', slug=slug)
    return render(render, 'blog/post/detail.html', {'post': post})
