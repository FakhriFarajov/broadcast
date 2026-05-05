from django.contrib import admin

from .models import Article, ArticleComment, ArticleStats, Category

admin.site.register(Article)
admin.site.register(ArticleStats)
admin.site.register(Category)
admin.site.register(ArticleComment)
