from django import forms

class CommentForm(forms.Form):
    body = forms.CharField(max_length=256, label="Your Comment")\
    