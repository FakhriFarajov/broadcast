from django.shortcuts import render
from article.models import Article
from profile_user.models import UserProfile


# Create your views here.
def main_view(request):
    selected_category = request.GET.get('category')
    search_query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'date')
    
    # Get articles from database
    articles = Article.objects.all().select_related('category', 'author', 'stats')

    if selected_category:
        articles = articles.filter(category__name=selected_category)

    if search_query:
        from django.db.models import Q
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    if sort_by == 'popularity':
        # Top-to-bottom by likes.
        articles = articles.order_by('-stats__likes', '-created_on')
    else:
        sort_by = 'date'
        articles = articles.order_by('-created_on')

    # Get author profiles for each article
    articles_with_profiles = []
    for article in articles:
        author_profile, created = UserProfile.objects.get_or_create(user=article.author)
        if(article.is_confirmed == False):
            continue
        articles_with_profiles.append({
            'article': article,
            'author_profile': author_profile
        })

    # Get first article for hero section
    featured_article = None
    featured_author_profile = None
    if articles_with_profiles:
        featured_article = articles_with_profiles[0]['article']
        featured_author_profile = articles_with_profiles[0]['author_profile']

    context = {
        'articles': articles,
        'articles_with_profiles': articles_with_profiles,
        'featured_article': featured_article,
        'featured_author_profile': featured_author_profile,
        'sort_by': sort_by,
    }
    return render(request, 'main/main_view.html', context)
