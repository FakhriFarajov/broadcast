from django.shortcuts import render
from article.data import ARTICLES

# Create your views here.
def main_view(request):
    return render(request, 'main/main_view.html', {'articles': ARTICLES})