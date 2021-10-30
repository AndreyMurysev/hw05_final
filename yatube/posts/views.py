from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect

from .forms import CommentForm, PostForm
from .models import Follow, Group, Like, Post, User

PAGINATOR_LIST = settings.PAGINATOR_LIST


@cache_page(20, key_prefix='index_page')
def index(request):
    """
    Сортирует по дате посты в базе и вывводит 30 результатов.
    """
    latest = Post.objects.all()[:30]
    paginator = Paginator(latest, PAGINATOR_LIST)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'posts/index.html', {'page': page})


def group_posts(request, slug):
    """
    Прнимает название сообщества и выводит последнии 30 записей
    get_object_or_404 ищет в базе объект модели и если не находит
    — прерывает работу view-функции и возвращает страницу с ошибкой 404.
    """
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('group').all()[:30]
    paginator = Paginator(posts, PAGINATOR_LIST)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'group': group, 'love_game': True}
    return render(request, 'posts/group.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('group').all()
    paginator = Paginator(posts, PAGINATOR_LIST)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    current_path = request.get_full_path()
    following = Follow.objects.filter(
        user_id=request.user.id,
        author_id=author.id).exists()
    context = {
        'author': author,
        'page': page,
        'current_path': current_path,
        'following': following}
    return render(request, 'posts/profile.html', context)


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = author.posts.select_related('group').get(pk=post_id)
    form = CommentForm(request.POST or None)
    current_path = request.get_full_path()
    like = Like.objects.filter(
        user_id=request.user.id,
        post_id=post.id).exists()
    context = {
        'post': post,
        'current_path': current_path,
        'author': author,
        'form': form,
        'like': like}
    return render(request, 'posts/post.html', context)


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('post', username=post.author, post_id=post.pk)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if request.method == 'POST' and form.is_valid():
        post.save()
        return redirect('post', username=request.user, post_id=post.pk)
    current_path = request.get_full_path()
    context = {
        'form': form,
        'post': post,
        'current_path': current_path}
    return render(request, 'posts/new.html', context)


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save(request.user)
        return redirect('index')
    return render(request, 'posts/new.html', {'form': form})


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(request.user, post)
        return redirect('post', username, post_id)
    context = {'form': form, 'post': post}
    return render(request, 'includes/comments.html', context)


@login_required
def follow_index(request):
    current_user = get_object_or_404(User, id=request.user.id)
    author_following = current_user.follower.all().values_list('author_id')
    latest = Post.objects.filter(author_id__in=author_following)[:30]
    paginator = Paginator(latest, PAGINATOR_LIST)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'follow': True}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if (author.id != request.user.id
        and not Follow.objects.filter(
            author=author,
            user=request.user).exists()):
        Follow.objects.create(user_id=request.user.id, author_id=author.id)
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    profile = get_object_or_404(User, username=username)
    Follow.objects.filter(
        user_id=request.user.id,
        author_id=profile.id).delete()
    return redirect('profile', username)

@login_required
def like_follow(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = get_object_or_404(User, username=username)
    like = Like.objects.filter(
        user_id=request.user.id,
        post_id=post.id).exists()
    if like:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    Like.objects.create(
        user_id=request.user.id,
        author_id=author.id,
        post_id=post.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

