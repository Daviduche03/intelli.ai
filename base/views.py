from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserForm, MyForm
from .models import Template, User
from django.http import JsonResponse
import openai
#from .models import Room, Topic, Message, User

openai.api_key = "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"

def generate_content(form_data):
    # Get the prompt style from the form data
    prompt_style = form_data['prompt_style']

    # Define a dictionary of prompt styles, where each key is a prompt style and the corresponding value is a dictionary
    # containing the prompt text and model to use for that prompt style
    prompt_styles = {
        'fix_grammar': {
            'prompt': "Please fix the grammar in this sentence: " + form_data['description'],
            'model': "text-davinci-002",
            'n': 1
        },
        'blog_outline': {
            'prompt': "Generate an outline for a blog post about " + form_data['topic'],
            'model': "text-davinci-002",
            'n': 5
        },
        'fb_ad': {
            'prompt': "Generate a Facebook ad template for a product called " + form_data['topic'] + " with the following description: " + form_data['description'] + " Write in a " + form_data['tone'] + " tone.",
            'model': "text-davinci-002",
            'n': 5
        },
        'creative_writing': {
            'prompt': "Generate a creative article with the topic " + form_data['topic'] + " using the following description: " + form_data['description'] + "  in a " + form_data['tone'] + " tone.",
            'model': "text-davinci-002",
            'n': 4
        },
        'blog_topic': {
            'prompt': "Generate a list of topic for a blog post in the following description: " + form_data['description'],
            'model': "text-davinci-002",
            'n': 5
        },
        'blog_post_intro': {
            'prompt': "Generate an introductory paragraph for a blog post with the topic " + form_data['topic'] + " using the following description: " + form_data['description'] + " in a " + form_data['tone'] + " tone.",
            'model': "text-davinci-002",
            'n': 4
        },
        'product_description': {
            'prompt': "Generate a description a product called " + form_data['topic'] + " using the following description: " + form_data['description'] + " in a " + form_data['tone'] + " tone.",
            'model': "text-davinci-002",
            'n': 5
        },
        'email': {
            'prompt': "write a " + form_data['tone'] + " email with the description: " + form_data['description'] + " to " + form_data['topic'] + " .",
            'model': "text-davinci-002",
            'n': 5
        },
        'content_improver': {
            'prompt': "improve the following content " + form_data['description'] + " in a " + form_data['tone'] + " tone.",
            'model': "text-davinci-002",
            'n': 1
        },
        'Content creation': {
             'prompt': "Generate a unique and engaging blog post on the topic of" + form_data['topic'] + "with a minimum length of 800 words",
             'model': "text-davinci-002",
             'n': 5
        }
        
        
        # Add more prompt styles here...
        }

    # Look up the prompt text and model for the selected prompt style in the prompt_styles dictionary
    prompt = prompt_styles[prompt_style]['prompt']
    model = prompt_styles[prompt_style]['model']
    n = prompt_styles[prompt_style]['n']

    # Use the model to generate content for the prompt
    completions = openai.Completion.create(engine=model, prompt=prompt, n=n, max_tokens=1024)

    # Return the generated content
    #return completions.choices[0].text
    
    return completions.choices



# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    
    return render(request, 'base/login.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserForm()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = MyUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect ('home')
            else:
                messages.error(request, 'error while registering user')

        
    return render(request, 'base/register.html', {'form': form})


def home(request):
    return render(request, 'base/index.html')


def templates(request):
    templates = Template.objects.all()
    
    context = {
    'templates' : templates
    }
    return render(request, 'base/templates.html', context)
    

def new(request):
    #template = Template.objects.get(slug=slug_url)
    
    if request.method == 'POST':
        # If the form has been submitted, process the form data
        form = MyForm(request.POST)
        
        if form.is_valid():
            
            # If the form is valid, generate content using the generate_content function
            content = generate_content(form.cleaned_data)
            data = {'content': content}
            return JsonResponse(data)
    else:
        # If the form has not been submitted, create a new form
        form = MyForm()
        
        
    return render(request, 'base/product.html', {'form': form})


def totalUser(request):
    if request.user.is_superuser:
        user = User.objects.all()
        total =  user.count()
        
        return render(request, 'base/users.html', {'total': total})
    else:
        return HttpResponseNotFound('Access denied!!!!')