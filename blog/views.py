from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *


def index(request):
    return render(request, 'blog/index.html')


def success_ticket(request):
    return render(request, 'blog/success_ticket.html')


def post_list(request, category=None):
    if category:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # posts = paginator.page(page_number)
    return render(request, 'blog/post_list.html', {'posts': posts, 'category': category})


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


@login_required
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
            result1 = (Post.published.annotate(
                similarity=TrigramSimilarity('title', query) +
                           TrigramSimilarity('description', query))
                       .filter(similarity__gt=0.1).values('id', 'title', 'similarity'))  # Add 'id' here.
            result2 = (Image.objects.annotate(
                similarity=TrigramSimilarity('title', query) +
                           TrigramSimilarity('description', query))
                       .filter(similarity__gt=0.1).values('id', 'title', 'similarity'))  # Add 'id' here.

            results = (result1.union(result2)).order_by('-similarity')

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'blog/search.html', context)


@login_required
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    return render(request, 'blog/profile.html', {'posts': posts})


@login_required
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


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile')

    return render(request, 'forms/delete_post.html', {'post': post})


@login_required
def delete_image(request, img_id):
    image = get_object_or_404(Image, id=img_id)
    image.delete()
    return redirect('blog:profile')


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm(instance=post)

    return render(request, 'forms/create_post.html', {'form': form, 'post': post})


def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'registration/register_done.html', {'user': user})

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def edit_account(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        account_form = AccountEditForm(instance=request.user.account, data=request.POST, files=request.FILES)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)
    context = {
        'user_form': user_form,
        'account_form': account_form,
        }
    return render(request, 'registration/edit_account.html', context)


