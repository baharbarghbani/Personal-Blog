from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your name (optional)",
                "class": "comment-name-input",
                "autocomplete": "name",
            }
        ),
    )
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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields.pop("name")

    class Meta:
        model = Comment
        fields = ("name", "body")
