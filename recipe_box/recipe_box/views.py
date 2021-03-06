from django.shortcuts import render, HttpResponseRedirect, reverse
from recipe_box.models import Author, Recipe, User
from recipe_box.forms import RecipeAddForm, AuthorAddForm
from recipe_box.forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    recipes = Recipe.objects.all()
    return render(request, 'index.html', {'data':recipes})

def recipe(request, r_id):
    recipe_id = Recipe.objects.get(id=r_id)
    return render(request, 'recipe.html', {'data':recipe_id})

def author(request, a_id):
    author_recipes = Recipe.objects.filter(author=a_id)
    return render(request, 'author.html', {'data':author_recipes})

@login_required()
def recipeadd(request):
    html = 'recipeadd.html'
    form = None

    if request.method == "POST":
        form = RecipeAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            Recipe.objects.create(
                title=data['title'],
                description=data['description'],
                time=data['time'],
                instructions=data['instructions'],
                author=data['author']
            )
            return render(request, 'thanks.html')
    else:
        form = RecipeAddForm

    return render(request, html, {'form': form})

@staff_member_required()
def authoradd(request):
    html = 'authoradd.html'
    form = None

    if request.method == "POST":
        form = AuthorAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username = data['username']
            )
            Author.objects.create(
                bio=data['bio'],
                user=user,
                name=data['name']
            )
            return render(request, 'thanks.html')
    else:
        form = AuthorAddForm

    return render(request, html, {'form': form})

def signup_view(request):
    html = 'signup.html'
    form = None

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'], data['password'])
            login(request, user)
            Author.objects.create(
                bio=data['bio'],
                user=user,
                name=data['name']
            )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = SignupForm()

    return render(request, html, {'form': form})

    
def login_view(request):
    html = 'signup.html'
    form = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
    