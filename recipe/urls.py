from django.urls import path
from .views import add_ingredients, add_instructions, recipe, recipe_details, delete_recipe, edit_recipe

urlpatterns = [
    path('create-recipe/', recipe, name='create_recipe'),
    path('create-recipe/<slug:recipe_slug>/', recipe, name='create_recipe'),
    path("create-recipe/<slug:recipe_slug>/add-ingredients/", add_ingredients, name="add_ingredients"),
    path("create-recipe/<slug:recipe_slug>/add-instructions/", add_instructions, name="add_instructions"),
    path("recipe-details/<slug:category_slug>/<slug:recipe_slug>/", recipe_details, name="recipe_details"),
    path("delete-recipe/<slug:category_slug>/<slug:recipe_slug>/", delete_recipe, name="delete_recipe"),
    path("edit-recipe/<slug:category_slug>/<slug:recipe_slug>/", edit_recipe, name="edit_recipe"),
]
