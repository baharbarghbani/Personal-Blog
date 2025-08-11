from django import forms

class ContactForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='Your Name', help_text="Please enter your full name.")
    subject = forms.CharField(max_length=30, required=True, label='Subject')
    email = forms.EmailField(required=True, label='Your Email', help_text="Please enter a valid email.")
    message = forms.CharField(widget=forms.Textarea, required=True, label='Your Message')
