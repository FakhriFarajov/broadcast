from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from article.models import Article, SavedArticle
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile_view(request):
    user_created_articles = Article.objects.filter(author=request.user)
    user_saved_articles = SavedArticle.objects.filter(user=request.user)

    count_views = sum(article.stats.views if hasattr(article, 'stats') else 0 for article in user_created_articles)

    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Handle form submission
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile:profile')
    else:
        form = UserProfileForm(instance=user_profile, user=request.user)

    context = {
        'user': request.user,
        'user_profile': user_profile,
        'form': form,
        'articles': user_created_articles,
        'articles_created_count': user_created_articles.count(),
        'articles_saved_count': user_saved_articles.count(),
        'total_views': count_views,
    }
    return render(request, 'profile/profile.html', context)


@login_required
def saved_articles_view(request):
    user_created_articles = Article.objects.filter(author=request.user)
    user_saved_articles = Article.objects.filter(saved_by__user=request.user).select_related('category', 'author').distinct()

    count_views = sum(article.stats.views if hasattr(article, 'stats') else 0 for article in user_created_articles)

    context = {
        'user': request.user,
        'saved_articles': user_saved_articles,
        'articles': user_saved_articles,
        'articles_created_count': user_created_articles.count(),
        'articles_saved_count': user_saved_articles.count(),
        'total_views': count_views,
    }
    return render(request, 'profile/saved_articles.html', context)


@login_required
def edit_profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile:profile')
    else:
        form = UserProfileForm(instance=user_profile, user=request.user)
    
    context = {
        'user': request.user,
        'user_profile': user_profile,
        'form': form,
    }
    return render(request, 'profile/edit_profile.html', context)
