from django import forms
from .models import Comment


# a form on it's own
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(max_length=250,
                               required=False,
                               widget=forms.Textarea)


# a form specifically for a model (in this case Comment)
class CommentForm(forms.Form):
    class Meta:
        # specify the assofiated model
        model = Comment
        # specify which fields to use only - if not specified will use all
        fields = ('name', 'email', 'body')
