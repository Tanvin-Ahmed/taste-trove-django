from django import forms  
from .models import Ingredient, Instruction, Recipe

class RecipeForm(forms.ModelForm):  
    class Meta:   
        model = Recipe  
        fields = ['recipe_name', 'slug', 'descriptions', 'image', 'category'] 


class IngredientForm(forms.ModelForm): 
    class Meta: 
        model = Ingredient
        fields = ['ingredient']


class InstructionForm(forms.ModelForm): 
    class Meta: 
        model = Instruction
        fields = ['step_no', 'instruction']