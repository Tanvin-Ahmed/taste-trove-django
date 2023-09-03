from django.contrib import admin
from .models import Recipe, Ingredient, Instruction
# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('recipe_name',)}
    list_display = ['recipe_name', 'slug']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['ingredient']


class InstructionAdmin(admin.ModelAdmin):
    list_display = ['instruction']

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Instruction, InstructionAdmin)