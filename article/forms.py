from django import  forms
from django.core.exceptions import ValidationError

class CreateNewsForm(forms.Form):
    title = forms.CharField(label="Title", required=True, max_length=120, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Description", required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    content = forms.CharField(label="Content", required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(label="Image", required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    author = forms.CharField(label="Author", required=True, max_length=120, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.CharField(label="Category", required=True, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_title(self):
        title = self.cleaned_data['title']
        banned_words = ["nigger", "nigga"]
        for i in banned_words:
            if i in title.lower():
                raise ValidationError("Title contains banned words")
        return title

    def clean_category(self):
        category = self.cleaned_data['category']
        banned_words = ["nigger", "nigga"]
        for i in banned_words:
            if i in category.lower():
                raise ValidationError("category contains banned words")
        return category

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

    def clean_author(self):
        author = self.cleaned_data['author']
        banned_words = ["nigger", "nigga"]
        for i in banned_words:
            if i in author.lower():
                raise ValidationError("Author contains banned words")
        return author

