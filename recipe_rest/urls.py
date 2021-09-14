from django.urls import path
from . import views

urlpatterns = [
    path("recipes/", views.RecipeApiView.as_view(), name="recipes"),
    path("user/", views.UserApiView.as_view(), name="user"),
]


from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'recipe', views.RecipeViewset, basename='recipe'),

urlpatterns += router.urls
