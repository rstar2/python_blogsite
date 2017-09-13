from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):

    title = 'Blog feeds'
    link = '/blog/'
    description = 'New post on the blog'

    def items(self):
        return Post.status_published.all()[:5]

    def item_title(self, post: Post):
        return post.title

    def item_description(self, post: Post):
        return truncatewords(post.body, 30)
