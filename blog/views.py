from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *


def index(request):
    return HttpResponse("INDEX")


def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)

