from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


# Create your views here.

def post_list(request):
    posts_all = Post.status_published.all()

    # add pagination - 3 posts per page
    paginator = Paginator(posts_all, 3)
    # get requested page number
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer then deliver the FIRST page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range then deliver the LAST page
        posts = paginator.page(paginator.num_pages)

    print(page)
    return render(request, 'blog/post/list.html', {'posts': posts,
                                                   'page': page})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, status='published', slug=slug,
                             published__year=year,
                             published__month=month,
                             published__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})
