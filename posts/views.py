from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import PostForm, CommentForm


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
    posts = Post.objects.all().order_by('-created_at')
    return render(request, "posts/post.html", {
        "posts": posts,
    })


@login_required
def single_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    comment_form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "user_liked_post": request.user in post.likes.all(),
        "user_liked_comments": [comment.id for comment in comments if request.user in comment.likes.all()]
    }

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()
            return redirect('single_post', post_id=post_id)

    return render(request, "posts/single_post.html", context)


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


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, created_by=request.user)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('single_post', post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, "posts/edit_comment.html", {"form": form, "comment": comment})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, created_by=request.user)
    if request.method == "POST":
        comment.delete()
    return redirect('single_post', post_id=post_id)


@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'likes_count': post.likes.count(),
        'liked': liked
    })


@login_required
@require_POST
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'likes_count': comment.likes.count(),  # Use direct count instead of method
        'liked': liked
    })
