from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark border-dev text-white',
            'placeholder': 'Username'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control bg-dark border-dev text-white',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.username = self.cleaned_data.get('username')
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile
