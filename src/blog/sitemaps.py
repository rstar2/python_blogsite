from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):

    # each attribute can also be a method, e.g:
    # def priority(self):
    #     return 0.9
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.status_published.all()

    def lastmod(self, obj: Post):
        return obj.published
