from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        max_length=255,
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Write your comment here...",
                "class": "comment-input",
            }
        ),
    )

    class Meta:
        model = Comment
        fields = ("body",)
