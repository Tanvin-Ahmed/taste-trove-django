from django.urls import path
from home.views import home

urlpatterns = [
    path('', home, name='home'),
    path("category/<slug:category_slug>/", home, name="recipes_by_category"),
]