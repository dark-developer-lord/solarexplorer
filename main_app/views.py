from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm, ForumThreadForm, ForumPostForm
from .models import CustomUser, ForumThread, ForumPost, NewsArticle, TeamMember, ForumCategory
from rest_framework_simplejwt.tokens import RefreshToken
import random

def home(request):
    users = CustomUser.objects.all()[:10]
    users_with_data = [
        {
            'username': user.username,
            'email': user.email,
            'border_color': f'hsl({(index * 60) % 360}, 70%, 60%)',
            'profile_photo': user.profile_photo.url if user.profile_photo else '/static/hackathon/images/default-user.jpg',
            'stats': {
                'posts': ForumPost.objects.filter(created_by=user).count(),
                'threads': ForumThread.objects.filter(created_by=user).count(),
                'random_delay': random.uniform(0, 2)
            }
        }
        for index, user in enumerate(users)
    ]
    context = {
        'team_members': TeamMember.objects.all(),
        'users': users_with_data,
        'disclaimer': 'NASA does not endorse any non-U.S. Government entity.',
        'user': request.user if request.user.is_authenticated else None,
    }
    return render(request, 'hackathon/home.html', context)

def register_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return redirect('home?success=register')
        else:
            return render(request, 'hackathon/registration.html', {'form': form, 'error': 'Invalid input'})
    else:
        form = CustomUserCreationForm()
    return render(request, 'hackathon/registration.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return redirect('home?success=login')
            else:
                return render(request, 'hackathon/login.html', {'form': form, 'error': 'Invalid credentials'})
        else:
            return render(request, 'hackathon/login.html', {'form': form, 'error': 'Invalid input'})
    else:
        form = LoginForm()
    return render(request, 'hackathon/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def user_profile(request):
    return render(request, 'hackathon/profile.html', {'user': request.user})

@login_required
def forum_main(request):
    categories = ForumCategory.objects.all()
    threads = ForumThread.objects.all().order_by('-created_at')
    category_filter = request.GET.get('category', '')
    if category_filter:
        threads = threads.filter(category__name=category_filter)
    if request.method == 'POST':
        form = ForumThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.created_by = request.user
            thread.save()
            return redirect('forum_main')
    else:
        form = ForumThreadForm()
    context = {'categories': categories, 'threads': threads, 'form': form}
    return render(request, 'hackathon/forum.html', context)

@login_required
def forum_thread(request, thread_id):
    thread = get_object_or_404(ForumThread, id=thread_id)
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.created_by = request.user
            post.save()
            thread.views += 1
            thread.save()
            return redirect('forum_thread', thread_id=thread_id)
    else:
        form = ForumPostForm()
    context = {'thread': thread, 'form': form, 'posts': thread.posts.all()}
    return render(request, 'hackathon/forum_thread.html', context)

def news_list(request):
    articles = NewsArticle.objects.all().order_by('-created_at')
    category_filter = request.GET.get('category', '')
    if category_filter:
        articles = articles.filter(category=category_filter)
    context = {'articles': articles, 'categories': NewsArticle.objects.values('category').distinct()}
    return render(request, 'hackathon/news.html', context)

def news_detail(request, news_id):
    article = get_object_or_404(NewsArticle, id=news_id)
    article.views += 1
    article.save()
    return render(request, 'hackathon/news_detail.html', {'article': article})

def nasa_analytics(request):
    return render(request, 'hackathon/nasa_analytics.html', {})

def ai_demo(request):
    return render(request, 'hackathon/ai_demo.html', {})