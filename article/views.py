# region Production
# from django.shortcuts import render, redirect
# from article.forms import CreateNewsForm
# from django.http import JsonResponse
# import cloudinary.uploader
#
# from article.models import Article
#
# import data
#
# # Create your views here.
# def article_view(request):
#     return render(request, "article/article.html", {"article": data.get_articles()})
#
# def create_article(request):
#     if request.method == 'POST':
#         form = CreateNewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             image_url = None
#             image_file = form.cleaned_data.get('image')
#             if image_file:
#                 upload_result = cloudinary.uploader.upload(image_file)
#                 image_url = upload_result.get('url')
#                 print(image_url)
#             return render(request, "article/article.html", {"image_url": image_url})
#     else:
#         form = CreateNewsForm()
#     return render(request, "article/create_article.html", {"form": form})

# endregion


from django.shortcuts import render, redirect
from article.forms import CreateNewsForm
import cloudinary.uploader
from article.data import get_article, create_article as create_article_data
from datetime import datetime

# Create your views here.
def article_view(request):
    article = get_article(0)
    return render(request, "article/article.html", {"article": article})

def create_article(request):
    if request.method == 'POST':
        form = CreateNewsForm(request.POST, request.FILES)
        if form.is_valid():
            image_url = None
            image_file = form.cleaned_data.get('image')
            if image_file:
                upload_result = cloudinary.uploader.upload(image_file)
                image_url = upload_result.get('url')
            article = create_article_data(
                form.cleaned_data['title'],
                form.cleaned_data['content'],
                form.cleaned_data['description'],
                image_url,
                form.cleaned_data['category'],
                form.cleaned_data['author'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            return redirect('article:article')
    else:
        form = CreateNewsForm()
    return render(request, "article/create_article.html", {"form": form})
