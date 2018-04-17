from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from menu_planner.views import IngestedRecipeViewset

# router = DefaultRouter()
# router.register(r'ingested_recipes', IngestedRecipeViewset, base_name='ingested')

# urlpatterns = router.urls
urlpatterns = []
urlpatterns.append(path('admin/', admin.site.urls))
