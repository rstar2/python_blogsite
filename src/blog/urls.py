from django.conf.urls import url

from . import views

urlpatterns = [
    # name="blog_list" -> name of the URL to be used in HTML templates for instance
    url(r'^$', views.post_list, name="post_list"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.post_detail, name='post_detail')
]
