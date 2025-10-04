from django import forms

class CommentForm(forms.Form):
    body = forms.CharField(max_length=255, label="", widget=forms.Textarea(attrs={'placeholder': 'Write your comment here...', 'class': 'comment-input'}))
    