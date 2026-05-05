from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

import cloudinary.uploader

from article.forms import CreateNewsForm, EditArticleForm, CreateComment
from article.models import Article, ArticleReaction, ArticleStats, ArticleComment,SavedArticle
from profile_user.models import UserProfile


def article_view(request, id):
    article = get_object_or_404(Article, id=id)

    if(article.is_confirmed == False):
        return redirect("main:main")

    stats= ArticleStats.objects.get(article=article)
    # F("views") + 1 = "take current views count + 1, directly in the database"
    ArticleStats.objects.filter(article=article).update(views=F("views") + 1)
    stats.refresh_from_db()

    comments = ArticleComment.objects.filter(article=article).all().order_by("-created_on")

    # Get or create author's profile
    author_profile, created = UserProfile.objects.get_or_create(user=article.author)

    # Get profiles for all comment authors
    comments_with_profiles = []
    for comment in comments:
        comment_author_profile, created = UserProfile.objects.get_or_create(user=comment.author)
        comments_with_profiles.append({
            'comment': comment,
            'author_profile': comment_author_profile
        })

    current_reaction = None
    is_saved = False
    if request.user.is_authenticated:
        reaction = ArticleReaction.objects.filter(user=request.user, article=article).first()
        if reaction:
            current_reaction = reaction.reaction
        is_saved = SavedArticle.objects.filter(user=request.user, article=article).exists()

    context = {
        "article": article,
        "stats": stats,
        "comments": comments_with_profiles,
        "comment_count": comments.count(),
        "current_reaction": current_reaction,
        "is_saved": is_saved,
        "comment_form": CreateComment(),
        "author_profile": author_profile,
    }
    return render(request, "article/article.html", context)

@login_required
@transaction.atomic
def react_article(request, id, reaction_type):
    if request.method != "POST":
        return redirect("article:article_by_id", id=id)

    if reaction_type not in {ArticleReaction.LIKE, ArticleReaction.DISLIKE}:
        return redirect("article:article_by_id", id=id)

    article = get_object_or_404(Article, id=id)
    stats = ArticleStats.objects.get(article=article)

    existing = ArticleReaction.objects.filter(user=request.user, article=article).first()

    # Toggle same reaction off, or switch between like/dislike.
    if existing:
        if existing.reaction == reaction_type:
            existing.delete()
        else:
            existing.reaction = reaction_type
            existing.save(update_fields=["reaction", "updated_on"])
    else:
        ArticleReaction.objects.create(user=request.user, article=article, reaction=reaction_type)

    stats.likes = ArticleReaction.objects.filter(article=article, reaction=ArticleReaction.LIKE).count()
    stats.dislikes = ArticleReaction.objects.filter(article=article, reaction=ArticleReaction.DISLIKE).count()
    stats.save(update_fields=["likes", "dislikes"])

    return redirect("article:article_by_id", id=id)

@login_required
def create_article(request):
    if request.method == "POST":
        form = CreateNewsForm(request.POST, request.FILES)
        if form.is_valid():
            image_url = None
            image_file = form.cleaned_data.get("image")
            if image_file:
                upload_result = cloudinary.uploader.upload(image_file)
                image_url = upload_result.get("url")

            article = Article.objects.create(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                description=form.cleaned_data["description"],
                image_link=image_url,
                category=form.cleaned_data["category"],
                author=request.user if request.user.is_authenticated else None,
            )

            ArticleStats.objects.create(article=article, views=0, likes=0, dislikes=0)
            return redirect("main:main")
    else:
        form = CreateNewsForm()
    return render(request, "article/create_article.html", {"form": form})

@login_required
def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    
    if article.author != request.user:
        return redirect("article:article_by_id", id=id)
    
    if request.method == "POST":
        form = EditArticleForm(request.POST, request.FILES)
        if form.is_valid():
            image_url = article.image_link
            image_file = form.cleaned_data.get("image")
            
            if image_file:
                upload_result = cloudinary.uploader.upload(image_file)
                image_url = upload_result.get("url")
            
            article.title = form.cleaned_data["title"]
            article.content = form.cleaned_data["content"]
            article.description = form.cleaned_data["description"]
            article.image_link = image_url
            article.category = form.cleaned_data["category"]
            article.save()
            
            return redirect("article:article_by_id", id=id)
    else:
        form = EditArticleForm(initial={
            "title": article.title,
            "description": article.description,
            "content": article.content,
            "category": article.category,
        })
    
    return render(request, "article/edit_article.html", {"form": form, "article": article})

@login_required
def save_article(request, id):
    if request.method != "POST":
        return redirect("article:article_by_id", id=id)

    article = get_object_or_404(Article, id=id)
    saved_article = SavedArticle.objects.filter(article=article, user=request.user).first()

    # Toggle save/unsave.
    if saved_article:
        saved_article.delete()
    else:
        SavedArticle.objects.create(article=article, user=request.user)

    return redirect("article:article_by_id", id=id)

@login_required
def create_comment(request, id):
    if request.method != "POST":
        return redirect("article:article_by_id", id=id)

    article = get_object_or_404(Article, id=id)
    form = CreateComment(request.POST)

    if form.is_valid():
        ArticleComment.objects.create(
            article=article,
            comment=form.cleaned_data["comment"],
            author=request.user,
        )
        return redirect("article:article_by_id", id=id)

    # Re-render article page with comment form errors.
    stats = ArticleStats.objects.get(article=article)
    comments = ArticleComment.objects.filter(article=article).all().order_by("-created_on")
    
    # Get or create author's profile
    author_profile, created = UserProfile.objects.get_or_create(user=article.author)

    # Get profiles for all comment authors
    comments_with_profiles = []
    for comment in comments:
        comment_author_profile, created = UserProfile.objects.get_or_create(user=comment.author)
        comments_with_profiles.append({
            'comment': comment,
            'author_profile': comment_author_profile
        })

    current_reaction = None
    is_saved = SavedArticle.objects.filter(user=request.user, article=article).exists()
    reaction = ArticleReaction.objects.filter(user=request.user, article=article).first()
    if reaction:
        current_reaction = reaction.reaction

    context = {
        "article": article,
        "stats": stats,
        "comments": comments_with_profiles,
        "comment_count": comments.count(),
        "current_reaction": current_reaction,
        "is_saved": is_saved,
        "comment_form": form,
        "author_profile": author_profile,
    }
    return render(request, "article/article.html", context)

def articles_filtered(request, filter):

    articles = Article.objects.filter(is_confirmed=True).select_related("category", "author", "stats")
    if(filter == "date"):
        articles = articles.order_by("-created_on")
    elif(filter == "popularity"):
        articles = articles.order_by("-stats__likes", "-created_on")

    articles_with_profiles = []
    for article in articles:
        author_profile, _ = UserProfile.objects.get_or_create(user=article.author)
        articles_with_profiles.append({
            "article": article,
            "author_profile": author_profile,
        })

    featured_article = articles_with_profiles[0]["article"] if articles_with_profiles else None
    featured_author_profile = articles_with_profiles[0]["author_profile"] if articles_with_profiles else None

    context = {
        "articles": articles,
        "articles_with_profiles": articles_with_profiles,
        "featured_article": featured_article,
        "featured_author_profile": featured_author_profile,
    }
    return render(request, "main/main_view.html", context)
