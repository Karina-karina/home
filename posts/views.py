from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Group, User
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_posts.order_by('-pub_date')[:12]
    return render(request, 'group.html', {'group': group, 'posts': posts})


@login_required
def new_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_author = author.author_posts.order_by('-pub_date')
    paginator = Paginator(posts_author, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html',
                  {'page': page, 'author': author, 'paginator': paginator})


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    posts_author = author.author_posts.order_by('-pub_date')
    post = get_object_or_404(author.author_posts, id=post_id)
    return render(request, 'post.html',
                  {'post': post, 'posts': posts_author, 'author': author})


def post_edit(request, username, post_id):
    edit = True
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(author.author_posts, id=post_id)
    if post.author != request.user:
        return redirect('post', username=post.author, post_id=post.id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post', username=post.author, post_id=post.id)
    return render(request, 'new_post.html', {'form': form, 'post': post, 'author': author, 'edit': edit})
