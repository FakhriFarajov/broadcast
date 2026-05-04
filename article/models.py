from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


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
    is_confirmed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="articles")
    image_link = models.URLField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="articles")
    minutes_read = models.PositiveIntegerField(default=5)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ["-created_on"]
        verbose_name_plural = "articles"
        verbose_name = "article"

    def __str__(self):
        return self.title


class ArticleStats(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name="stats")
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-views"]
        verbose_name_plural = "articles stats"
        verbose_name = "articles stats"


class SavedArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="saved_articles")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="saved_by")
    saved_on = models.DateTimeField(auto_now_add=True)


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments")

    class Meta:
        ordering = ["-created_on"]
        verbose_name = "article comment"
        verbose_name_plural = "article comments"

    def __str__(self):
        return f"Comment on {self.article.title}"


class ArticleReaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"
    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_reactions")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_reactions")
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "article"], name="unique_article_reaction_per_user"),
        ]

    def __str__(self):
        return f"{self.user} {self.reaction} {self.article_id}"


class CommentReaction(models.Model):
    LIKE = "like"
    DISLIKE = "dislike"
    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_reactions")
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name="comment_reactions")
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "comment"], name="unique_comment_reaction_per_user"),
        ]

    def __str__(self):
        return f"{self.user} {self.reaction} comment {self.comment_id}"
