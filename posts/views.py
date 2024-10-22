from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect("list_post")
    else:
        form = PostForm()

    return render(request, "posts/create_post.html", {"form": form})


@login_required
def home_view(request):
    posts = Post.objects.all()
    return render(request, "posts/post.html", {"posts": posts})


@login_required
def single_post_view(request, post_id):
    if request.method == "GET":
        post = get_object_or_404(Post, id=post_id)
        return render(request, "posts/single_post.html", {"post": post})

    if request.method == "POST":
        return redirect("list_post")


@login_required
def delete_single_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        print("Deleting post:", post.id)
        post.delete()
        return redirect("list_post")
    else:
        return redirect("list_post")


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("list_post")
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit_post.html", {"form": form, "post": post})
