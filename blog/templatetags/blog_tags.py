from django import template
from django.db.models import Count

from ..models import Post, Comment

register = template.Library()


@register.simple_tag(name='tp')
def total_posts():
    return Post.published.count()


@register.simple_tag(name='tc')
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag()
def last_post_date():
    return Post.published.last().publish


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=5):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts,
    }
    return context


@register.simple_tag
def popular_posts(count=5):
    return Post.published.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]


@register.filter(name='censor')
def censor(text):
    bad_words = ['عوضی', 'آشغال', 'خر']
    for word in bad_words:
        if word in text:
            text = text.replace(word, '*' * len(word))
    return text