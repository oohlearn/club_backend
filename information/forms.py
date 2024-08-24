from django import forms
from .models import Article, Image


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'tags_input']
        widgets = {
            'tags_input': forms.Textarea(attrs={'rows': 2}),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

