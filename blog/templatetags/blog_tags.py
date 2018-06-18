import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from taggit.models import Tag

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    q = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')
    return q[:count]


@register.simple_tag
def archives():
    return Post.published.dates('publish', 'month', order='DESC')[:]


@register.simple_tag
def all_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
