from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count
from taggit.models import Tag
from .models import Post
from .forms import EmailPostForm, CommentForm


def post_list(request, tag_slug=None):
    posts_all = Post.status_published.all()

    # if this is a tlist for all post tagged with given tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts_all = posts_all.filter(tags__in=[tag])

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

    return render(request, 'blog/post/list.html', {'posts': posts,
                                                   'page': page,
                                                   'tag': tag})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, status='published', slug=slug,
                             published__year=year,
                             published__month=month,
                             published__day=day)

    # get the cmments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # create a Comment object from the form BUT DON'T SAVE it to the database yet
            new_comment = comment_form.save(commit=False)
            # assign the Post associated with this Comment
            new_comment.post = post
            # save/commit to the database now
            new_comment.save()
    else:
        comment_form = CommentForm()

    # whether or not a comment was saved
    new_comment_saved = 'new_comment' in locals()

    # Get list with "similar" posts
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.status_published.filter(tags__in=post_tags_id). \
        exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')). \
        order_by('-same_tags', '-published')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'new_comment_saved': new_comment_saved,
                                                     'similar_posts': similar_posts})


def post_share(request, post_id):
    # retrieve the specified post
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # so this is when form is submitted (on POST)
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # so the form is valid

            # clean the form's data
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],
                                                                   cd['email'],
                                                                   post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,
                                                                     post_url,
                                                                     cd['name'],
                                                                     cd['comments'])
            # real sending of the email
            send_mail(subject, message, 'admin@blogsite.com', [cd['to']])

            sent = True
    else:
        # this is when form is to be displayed (on GET)
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'form': form,
                                                    'post': post,
                                                    'sent': sent})
