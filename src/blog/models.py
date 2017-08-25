from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

    def from_rumen(self):
        return self.get_queryset().filter(author__username='rumen')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    class Meta:
        ordering = ('-published',)

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    # if we add a custom query Manager and want to use the default
    # Post.objects.all().filter()... one we have to add it explicitly
    # It's goot to keep this the first registered Manager as
    # it's used as default in multiple other places
    objects = models.Manager()

    # create a custom query Manager,
    # thus we can use Post.status_published.all().filter()....
    # Also we can use Post.status_published.from_rumen()
    status_published = PublishedManager()

    # add the taggit manager, so now we can use Post.tags.all() (which is as if Tag.objects.all())
    # or for a specific Post - post.tags.all(), post.tags.add('music', 'sports')
    tags = TaggableManager()

    def __str__(self):
        return self.title

    # a convention method
    def get_absolute_url(self):
        # url is set to be:
        # url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        #          views.post_detail, name='post_detail')
        # so to reverse it we have to set 4 parameters
        return reverse('blog:post_detail', args=[self.published.year,
                                                 self.published.strftime('%m'),
                                                 self.published.strftime('%d'),
                                                 self.slug])


class Comment(models.Model):
    class Meta:
        ordering = ('created',)

    # 1. related_name 'comments' means that we can use
    # post.comments.all() - e.g a named related manager
    # if don't name it Django will implicitly set it to: 'comment_set', so
    # post.comment_set.all()
    # 2. related_query_name 'comment' means we can use it in filter fields like so
    # Post.objects.filter(comment__active=True)
    post = models.ForeignKey(Post, related_name='comments',
                             related_query_name='comment')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Comment by {} on "{}"'.format(self.name, self.post)
