from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from recipe.models import Recipe
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    return render(request, 'register.html', {'form':form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
                
        if user is not None:
            login(request, user)
            return redirect('profile')
        
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
        
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    
    return redirect('login')

def profile(request):
    if request.user.is_authenticated: 
        is_recipe_exist = Recipe.objects.filter(created_by=request.user).exists()
        my_recipes = None
        if is_recipe_exist:
            my_recipes = Recipe.objects.filter(created_by=request.user).order_by('-updated_date')
        
        paginator = Paginator(my_recipes, 6)
        page = request.GET.get('page')
        paged_recipes = paginator.get_page(page)
        return render(request, 'profile.html', {'my_recipes': paged_recipes})
    else:
        return redirect('login')