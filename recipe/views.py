from django.shortcuts import render, redirect, get_object_or_404
from recipe.forms import RecipeForm, IngredientForm, InstructionForm
from recipe.models import Recipe, Ingredient, Instruction
from django.db.models import Prefetch
from category.models import Category
from django.http import HttpResponse
# Create your views here.s


def recipe(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            recipe_form = RecipeForm(request.POST, request.FILES)

            if recipe_form.is_valid():
                cleaned_data = recipe_form.cleaned_data
                cleaned_data['created_by'] = user
                # Use commit=False to prevent immediate saving
                recipe = recipe_form.save(commit=False)
                recipe.created_by = cleaned_data['created_by']
                recipe.save()
                return render(request, 'create-recipe.html', {'form': recipe_form, 'recipe_slug': recipe.slug})
        else:
            recipe_form = RecipeForm()
        return render(request, 'create-recipe.html', {'form': recipe_form})

    else:
        return redirect('login')


def add_ingredients(request, recipe_slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = IngredientForm(request.POST)
            is_recipe_exist = Recipe.objects.filter(slug=recipe_slug).exists()
            if is_recipe_exist:
                recipe = Recipe.objects.get(slug=recipe_slug)

                if form.is_valid():
                    ingredient_name = form.cleaned_data['ingredient']
                    existing_ingredients = Ingredient.objects.filter(
                        recipe__slug=recipe_slug, ingredient=ingredient_name)
                    if existing_ingredients.exists():
                        # Ingredient already exists for this recipe, add an error to the form
                        form.add_error(
                            'ingredient', 'This ingredient already exists for this recipe.')
                    else:
                        cleaned_data = form.cleaned_data
                        cleaned_data['recipe'] = recipe
                        # Use commit=False to prevent immediate saving
                        ingredient = form.save(commit=False)
                        ingredient.recipe = cleaned_data['recipe']
                        ingredient.save()

                        return render(request, 'add-ingredients.html', {'form': form, 'recipe_slug': recipe_slug, 'success_message': 'Ingredient added successfully'})
                else:
                    return render(request, 'add-ingredients.html', {'form': form, 'recipe_slug': recipe_slug, 'error_message': 'Something went wrong. Follow the instructions that given under input box'})
        else:
            form = IngredientForm()
        return render(request, 'add-ingredients.html', {'form': form, 'recipe_slug': recipe_slug})
    else:
        return redirect('login')


def add_instructions(request, recipe_slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = InstructionForm(request.POST)
            is_recipe_exist = Recipe.objects.filter(slug=recipe_slug).exists()
            if is_recipe_exist:
                recipe = Recipe.objects.get(slug=recipe_slug)

                if form.is_valid():
                    step_no = form.cleaned_data['step_no']
                    instruction_text = form.cleaned_data['instruction']
                    existing_no = Instruction.objects.filter(
                        recipe__slug=recipe_slug,
                        step_no=step_no,
                    )
                    existing_instructions = Instruction.objects.filter(
                        recipe__slug=recipe_slug,
                        instruction=instruction_text
                    )
                    if existing_instructions.exists():
                        # Instruction already exists for this recipe, add an error to the form
                        form.add_error(
                            'instruction', 'This instruction already exists for this recipe.')
                    elif existing_no.exists():
                        form.add_error(
                            'step_no', 'This step already exists for this recipe.')
                    else:
                        cleaned_data = form.cleaned_data
                        cleaned_data['recipe'] = recipe
                        # Use commit=False to prevent immediate saving
                        instruction = form.save(commit=False)
                        instruction.recipe = cleaned_data['recipe']
                        instruction.save()

                        return render(request, 'add-instructions.html', {'form': form, 'recipe_slug': recipe_slug, 'success_message': 'Instruction added successfully'})
                else:
                    return render(request, 'add-instructions.html', {'form': form, 'recipe_slug': recipe_slug, 'error_message': 'Something went wrong. Follow the instructions that given under input box'})
        else:
            form = InstructionForm()
        return render(request, 'add-instructions.html', {'form': form, 'recipe_slug': recipe_slug})
    else:
        return redirect('login')


def recipe_details(request, category_slug, recipe_slug):
    recipe = None
    if category_slug and recipe_slug:
        recipe = get_object_or_404(
            Recipe.objects.select_related('category', 'created_by')
            .prefetch_related('ingredient_set', Prefetch('instruction_set', queryset=Instruction.objects.order_by('step_no'))),
            category__slug=category_slug,
            slug=recipe_slug
        )
    return render(request, 'recipe-details.html', {'recipe': recipe})


def delete_recipe(request, category_slug, recipe_slug):
    if category_slug and recipe_slug:
        if request.user.is_authenticated:
            recipe = get_object_or_404(Recipe, category__slug=category_slug, slug=recipe_slug)
            if request.user == recipe.created_by:
                recipe.delete()
        else:
            return redirect('login')
            
    return redirect('profile')


def edit_recipe(request, category_slug, recipe_slug):
    # Get the recipe to edit
    recipe = get_object_or_404(Recipe, category__slug=category_slug, slug=recipe_slug)

    # Check if the user has permission to edit the recipe
    if request.user != recipe.created_by:
        return HttpResponse("Permission denied: You cannot edit this recipe")

    # Process the form submissions for recipe, ingredients, and instructions
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, instance=recipe)

        if recipe_form.is_valid():
            # Save the changes to the recipe, ingredients, and instructions
            recipe_form.save()

            # Redirect to the recipe detail page or another appropriate page
            return redirect('profile')

    else:
        recipe_form = RecipeForm(instance=recipe)

    context = {
        'recipe_form': recipe_form,
        'recipe': recipe,
    }

    return render(request, 'edit-recipe.html', context)