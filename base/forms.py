from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class MyUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        

class MyForm(forms.Form):
    prompt_style = forms.ChoiceField(choices=[
         ('Select a template', 'Select a Template Of Your Choice.'),
         ('Content creation', 'Content creation'),
        ('fix_grammar', 'Fix grammar in sentence'),
        ('blog_outline', 'Generate blog post outline'),
        ('fb_ad', 'Generate Facebook ad template'),
        ('creative_writing', 'Generate a creative content'),
        ('blog_topic', 'Generate a blog topic idea'),
        ('blog_post_intro', 'Generate a blog post intro paragraph'),
        ('product_description', 'Product Description'),
        ('email', 'Write an Email'),
        ('explain_like_am_5', "Explain like i'm 5"),
        ('content_improver', 'Content improver'),
        ('PAS', 'PAS framework')
        # Add more prompt tyles here...
    ], label="")
    topic = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Topic / Name"}))
    tone = forms.ChoiceField(choices=[
         ('Select a tone', 'Select The Template Tone.'),
        ('professional', 'Professional'),
        ('persuasive', 'Persuasive'),
        
        
    ], label="")
    description = forms.CharField(max_length=300,
     widget=forms.Textarea(attrs={"placeholder": "Description / Content"}), label="")
 