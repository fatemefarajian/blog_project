from django import template
from django.contrib.auth.models import User
from django.db.models import Count, Max

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


@register.simple_tag()
def max_reading_post():
    max_reading = Post.published.aggregate(Max('reading_time'))
    post_mr = Post.published.filter(reading_time=max_reading['reading_time__max']).first()
    return post_mr


@register.simple_tag()
def min_reading_post():
    return Post.published.order_by('reading_time').first()


@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=5):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts,
    }
    return context


@register.inclusion_tag('partials/active_users.html')
def show_active_users(count=2):
    active_users = User.objects.annotate(post_count=Count('user_posts')).order_by('-post_count')[:count]
    return {'active_users': active_users}

