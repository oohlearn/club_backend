from django import forms
from .models import Image, Article


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', "date", 'content', "status", "article_img"]
        widgets = {
            'tags_input': forms.Textarea(attrs={'rows': 2}),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
