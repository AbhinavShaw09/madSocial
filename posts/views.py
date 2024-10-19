from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

@login_required  # Ensure the user is logged in before creating a post
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Create post instance without saving to the database yet
            post.author = request.user  # Set the author to the logged-in user (optional)
            post.save()  # Now save the post to the database
            return redirect('list_post')  # Redirect to a list of posts after successful creation
    else:
        form = PostForm()
    
    return render(request, 'posts/create_post.html', {'form': form})

@login_required  # Ensure the user is logged in before accessing posts
def home_view(request):
    print("User is authenticated:", request.user.is_authenticated)
    posts = Post.objects.all()  # Fetch all posts from the database
    return render(request, 'posts/post.html', {'posts': posts})
