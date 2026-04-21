from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    content = models.TextField()
    image_link = models.URLField()
    author = models.CharField(max_length=120)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    tags = models.JSONField(default=list, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'articles'
        verbose_name = 'article'

class ArticleStats(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='stats')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-views']
        verbose_name_plural = 'articles stats'
        verbose_name = 'articles stats'

class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = "article comment"
        verbose_name_plural = "article comments"


    def __str__(self):
        return f"Comment on {self.article.title}"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name