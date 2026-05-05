from django import forms
from django.core.exceptions import ValidationError

from article.models import Category


class CreateNewsForm(forms.Form):
    title = forms.CharField(
        label="Title", 
        required=True, 
        max_length=120, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter article title'})
    )
    description = forms.CharField(
        label="Description", 
        required=True, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of the article'})
    )
    content = forms.CharField(
        label="Content", 
        required=True, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Full article content'})
    )
    category = forms.ModelChoiceField(
        label="Category", 
        required=True,
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label="Image",
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    def clean_title(self):
        title = self.cleaned_data['title']
        banned_words = ["nigger", "nigga"]
        for i in banned_words:
            if i in title.lower():
                raise ValidationError("Title contains banned words")
        return title


    def clean_content(self):
        content = self.cleaned_data['content']
        banned_words = ["nigger", "nigga"]
        for i in banned_words:
            if i in content.lower():
                raise ValidationError("Context contains banned words")
        return content

    def clean_description(self):
        description = self.cleaned_data['description']
        banned_words = ["nigger", "nigga"]
        for i in banned_words:
            if i in description.lower():
                raise ValidationError("Description contains banned words")
        return description

class EditArticleForm(forms.Form):
    title = forms.CharField(
        label="Title",
        required=True,
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter article title'})
    )
    description = forms.CharField(
        label="Description",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of the article'})
    )
    content = forms.CharField(
        label="Content",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Full article content'})
    )
    category = forms.ModelChoiceField(
        label="Category",
        required=True,
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label="Image",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    def clean_title(self):
        title = self.cleaned_data['title']
        banned_words = ["nigger", "nigga"]
        for i in banned_words:
            if i in title.lower():
                raise ValidationError("Title contains banned words")
        return title


    def clean_content(self):
        content = self.cleaned_data['content']
        banned_words = ["nigger", "nigga"]
        for i in banned_words:
            if i in content.lower():
                raise ValidationError("Context contains banned words")
        return content

    def clean_description(self):
        description = self.cleaned_data['description']
        banned_words = ["nigger", "nigga"]
        for i in banned_words:
            if i in description.lower():
                raise ValidationError("Description contains banned words")
        return description

class CreateComment(forms.Form):
    comment = forms.CharField(
        label="Comment",
        required=True,
        max_length=128,
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-3",
                "rows": 3,
                "placeholder": "Share your thoughts...",
                "style": "resize: vertical;",
            }
        ),
    )

    def clean_comment(self):
        banned_words = ["nigger", "nigga"]
        comment = self.cleaned_data['comment']
        for i in banned_words:
            if i in comment.lower():
                raise ValidationError("Comment contains banned words")
        return comment

