from django import forms
from django.forms import widgets
from .models import Comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
