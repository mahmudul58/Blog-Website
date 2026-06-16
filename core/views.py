from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import CreatePost, Comment, Topic, Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages

def index(request):
    featured_posts = CreatePost.objects.filter(is_featured=True).order_by('-created_at')[:3]
    latest_posts = CreatePost.objects.all().order_by('-created_at')[:6]
    return render(request, 'home/index.html', {'featured_posts': featured_posts, 'latest_posts': latest_posts})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            username = None
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'home/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
            
        if len(password) < 4:
            messages.error(request, "Password must be at least 4 characters long!")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
            return redirect('register')
            
        username = email.split('@')[0]
        if User.objects.filter(username=username).exists():
            username = email
            
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()
        
        Profile.objects.create(user=user)
        user = authenticate(request, username=username, password=password)
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('index')

    return render(request, 'home/register.html')

def post_detail(request, id):
    post = get_object_or_404(CreatePost, id=id)
    if request.method != "POST":
        if not request.user.is_authenticated or request.user != post.author:
            viewed_posts = request.session.get('viewed_posts', [])
            if post.id not in viewed_posts:
                post.view_count += 1
                post.save(update_fields=['view_count'])
                viewed_posts.append(post.id)
                request.session['viewed_posts'] = viewed_posts
    
    if request.method == "POST":
        if request.user.is_authenticated:
            content = request.POST.get("comment")
            if content:
                comment = Comment.objects.create(content=content, author=request.user, post=post)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'author_name': request.user.first_name or request.user.username,
                        'author_initial': request.user.username[0].upper(),
                        'content': comment.content,
                        'created_at': 'Just now'
                    })
                return redirect('post_detail', id=id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'You must be logged in to comment'}, status=403)
            messages.error(request, "You must be logged in to comment")
            return redirect('login')
            
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'home/post_detail.html', {'post': post, 'comments': comments})

@login_required
def like_post(request, id):
    post = get_object_or_404(CreatePost, id=id)
    if request.method == "POST":
        liked = False
        if request.user in post.liked_users.all():
            post.liked_users.remove(request.user)
        else:
            post.liked_users.add(request.user)
            liked = True
            
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'liked': liked, 'total_likes': post.total_likes()})
            
    return redirect('post_detail', id=id)

def archive(request):
    posts = CreatePost.objects.all().order_by('-created_at')
    return render(request, 'home/archive.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        topic_slug = request.POST.get('topic')
        cover_image_url = request.POST.get('cover_image_url')
        cover_image_file = request.FILES.get('cover_image_file')
        content = request.POST.get('content')

        if not title or not content or not topic_slug:
            messages.error(request, "Please fill in all required fields.")
            return redirect('create_post')

        topic_obj, created = Topic.objects.get_or_create(
            name__iexact=topic_slug.replace('-', ' '),
            defaults={'name': topic_slug.replace('-', ' ').title()}
        )

        post = CreatePost.objects.create(
            author=request.user,
            title=title,
            topic=topic_obj,
            cover_image_url=cover_image_url,
            cover_image=cover_image_file,
            content=content
        )
        
        messages.success(request, "Post created successfully!")
        return redirect('post_detail', id=post.id)

    return render(request, 'home/create_post.html', {'topics': Topic.objects.all()})

@login_required
def my_posts(request):
    posts = CreatePost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'home/my_posts.html', {'posts': posts})

@login_required
def edit_post(request, id):
    post = get_object_or_404(CreatePost, id=id, author=request.user)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        topic_id = request.POST.get('topic')
        custom_topic = request.POST.get('custom_topic')
        
        if topic_id == 'other' and custom_topic:
            topic, _ = Topic.objects.get_or_create(name=custom_topic)
            post.topic = topic
        elif topic_id and topic_id != 'other':
            post.topic = Topic.objects.get(id=topic_id)
            
        cover_image_url = request.POST.get('cover_image_url')
        if cover_image_url:
            post.cover_image_url = cover_image_url
            
        if 'cover_image_file' in request.FILES:
            post.cover_image = request.FILES['cover_image_file']
            
        post.content = request.POST.get('content')
        post.save()
        messages.success(request, "Post updated successfully!")
        return redirect('post_detail', id=post.id)
        
    return render(request, 'home/edit_post.html', {'post': post, 'topics': Topic.objects.all()})

@login_required
def delete_post(request, id):
    post = get_object_or_404(CreatePost, id=id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('my_posts')
    return redirect('my_posts')