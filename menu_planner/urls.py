from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from menu_planner.views import (IngestedRecipeViewset, RecipeViewset)

router = DefaultRouter()
router.register(r'ingested_recipes', IngestedRecipeViewset, base_name='ingested')
router.register(r'recipes', RecipeViewset, base_name='recipe')

urlpatterns = router.urls
urlpatterns.append(path('admin/', admin.site.urls))
