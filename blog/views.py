from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, TrigramSimilarity

from .models import *
from .forms import *


def index(request):
    return render(request, 'blog/index.html')


def success_ticket(request):
    return render(request, 'blog/success_ticket.html')


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    posts = paginator.page(page_number)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, "blog/post_detail.html", context)


def ticket(request):
    if request.method == 'POST':
        form = TicketForms(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(name=cd['name'],
                                  email=cd['email'],
                                  phone=cd['phone'],
                                  message=cd['message'],
                                  subject=cd['subject'])
            return redirect('blog:success_ticket')
    else:
        form = TicketForms()

    return render(request, 'forms/tickets.html', {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.name = request.user
        comment.save()
    context = {

        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, 'forms/comments.html', context)


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result1 = Post.published.annotate(similarity=TrigramSimilarity('title', query)) \
                .filter(similarity__gt=0.1)
            result2 = Post.published.annotate(similarity=TrigramSimilarity('description', query)) \
                .filter(similarity__gt=0.1)
            result3 = Image.objects.annotate(similarity=TrigramSimilarity('title', query)) \
                .filter(similarity__gt=0.1)
            result4 = Image.objects.annotate(similarity=TrigramSimilarity('description', query)) \
                .filter(similarity__gt=0.1)

            results = (result1 | result2 | result3 | result4).order_by('-similarity')
            # results = (Post.published.annotate(search=SearchVector('title', 'description'))
            #            .filter(search=query))
            # results = Post.published.filter(Q(title__search=query) | Q(description__search=query))

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'blog/search.html', context)


def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    return render(request, 'blog/profile.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form': form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile')

    return render(request, 'forms/delete_post.html', {'post': post})










