from django.shortcuts import render
from recipe.models import Recipe
from category.models import Category
from django.core.paginator import Paginator

# Create your views here.
def home(request, category_slug = None):
    categories = Category.objects.all()
    recipes = None
    ingredient = None
    if request.method == 'POST':
        ingredient = request.POST.get('ingredient', '')
        if ingredient:
            # Perform a case-insensitive search for recipes containing the specified ingredient
            recipes = Recipe.objects.filter(ingredient__ingredient__icontains=ingredient).order_by('-updated_date')
    elif category_slug:
        if Recipe.objects.filter(category__slug=category_slug).exists():
            recipes = Recipe.objects.filter(category__slug=category_slug).order_by('-updated_date')
    else:
        recipes = Recipe.objects.all().order_by('-updated_date')
    
    paginator = Paginator(recipes, 9)
    page = request.GET.get('page')
    paged_recipes = paginator.get_page(page)
    return render(request, 'home.html', {'recipes': paged_recipes, 'categories': categories, 'search_by':ingredient})

