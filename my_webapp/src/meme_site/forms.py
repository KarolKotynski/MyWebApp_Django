from django import forms
from .models import CommentSection


class CommentForm(forms.ModelForm):
    """
    creating class Meta where our model will be CommentSection from models.py
    and changed content form
    """
    class Meta:
        model = CommentSection
        widgets = {
            'content': forms.Textarea(attrs={
                'size': 2,
                'rows': 2,
                'cols': 60,
                'placeholder': 'Comment here!'
                }),
        }
        fields = ['content']

