from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # if we add a custom query Manager and want to use the default
    # Post.objects.all().filter()... one we have to add it explicitly
    # It's goot to keep this the first registered Manager as
    # it's used as default in multiple other places
    objects = models.Manager()

    # create a custom query Manager,
    # thus we can use Post.status_published.all().filter()....
    # Also we can use Post.status_published.from_rumen()
    status_published = PublishedManager()

    def __str__(self):
        return self.title
