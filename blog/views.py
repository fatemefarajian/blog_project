from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)


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






