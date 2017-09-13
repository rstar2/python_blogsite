from django import template
from django.utils.safestring import mark_safe
from django.db.models import Count

import markdown
from ..models import Post

register = template.Library()


# register a simple tag - used in a template with "{% get_total_posts %}"
@register.simple_tag
def get_total_posts():
    return Post.status_published.count()


# register an inclusion tag - used in a template with "{% show_latest_posts 3 %}"
@register.inclusion_tag('blog/post/_latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.status_published.order_by('-published')[:count]

    # inclusion-tags have to return a dictionary of values used as context
    # in the specified "inlcuded" template
    return {'latest_posts': latest_posts}


# register an assignment tag - used in a template with
# {% get_most_commented_posts 3 as mc_posts %}
# Since Django 1.9 simple-tags can be used as assignment-tags,
# e.g. to store their return value - so no need anymore for '@register.assignment_tag'
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.status_published.annotate(total_comments=Count('comment')). \
        order_by('-total_comments')[:count]


# register a simple filter - used in a template with {{ variable|markdown }}
@register.filter(name='markdown')
def filter_markdown(text):
    return mark_safe(markdown.markdown(text))
