from django.db import models
from category.models import Category
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint

# Create your models here.
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descriptions = models.TextField(blank=True)
    image = models.ImageField(upload_to="photos/recipe")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.recipe_name


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_in_recipe'
            )
        ]
    
    def __str__(self):
        return self.ingredient

class Instruction(models.Model):
    step_no = models.IntegerField()
    instruction = models.CharField(max_length=300)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['step_no', 'instruction', 'recipe'],
                name='unique_instruction_in_recipe'
            )
        ]
    
    def __str__(self):
        return self.instruction