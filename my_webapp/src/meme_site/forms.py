from django import forms
from .models import Comment_section

"""
creating class Meta where our model will be Comment_section from models.py
and changed content form
"""
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment_section
        widgets = {
            'content': forms.Textarea(attrs={
                'size': 2,
                'rows': 2,
                'cols': 60,
                'placeholder': 'Comment here!'
                }),
        }
        fields = ['content']

