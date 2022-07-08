from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGINATOR_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, settings.PAGINATOR_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "group": group,
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    author = User.objects.get(username=username)
    posts_user = Post.objects.filter(author_id=author).order_by("-pub_date")
    paginator = Paginator(posts_user, settings.PAGINATOR_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    user = request.user
    if user.is_authenticated:
        following = Follow.objects.filter(author=author, user=user).count()
    else:
        following = False
    context = {
        "page_obj": page_obj,
        "author": author,
        "following": following,
    }
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post).all()
    form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_id = request.user.id
            post.save()
            return redirect("posts:profile", username=request.user.username)
        return render(request, "posts/create_post.html", {"form": form})
    form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect("posts:post_detail", post_id=post_id)

    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author_id = request.user.id
        post.save()
        return redirect("posts:post_detail", post_id=post_id)
    context = {
        "post": post,
        "form": form,
        "is_edit": True,
    }
    return render(request, "posts/create_post.html", context)


@login_required
def post_delit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect("posts:post_detail", post_id=post_id)
    Post.objects.filter(pk=post.pk).delete()
    return redirect("posts:profile", username=post.author.username)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def delite_comment(request, post_id, pk):
    user = request.user
    author = Comment.objects.get(pk=pk)
    if user == author.author:
        author.delete()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
    user = request.user
    post_list = Post.objects.filter(author__following__user=user)
    paginator = Paginator(post_list, settings.PAGINATOR_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if len(post_list) == 0:
        following = False
    else:
        following = True
    context = {
        "page_obj": page_obj,
        "following": following,
    }
    return render(request, "posts/follow.html", context)


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user != author:
        Follow.objects.get_or_create(user=user, author=author)
    return redirect("posts:profile", username=username)


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(author=author, user=user).delete()
    return redirect("posts:index")
