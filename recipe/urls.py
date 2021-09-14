from django.urls import path
from . import views

urlpatterns =[
    path("login_form/", views.login_form, name="login_form"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("userform/", views.user_form, name="user_form"),
    path("saveuser/", views.saveuser, name="saveuser"),
    path("", views.recipe_booklet, name="recipe_booklet"),
    path("saverecepi/", views.saverecepi, name="saverecepi"),
    path("form/", views.register_recipe, name="register_recipe"),
    path("<int:recipe_id>/editrecipe/", views.editrecipe, name="edit_recipe"),
    path("<int:recipe_id>/deleterecipe/", views.deleterecipe, name="deleterecipe"),
    path("contact/", views.contact_form, name="contact_form"),
    path("detail/<int:recipe_id>/", views.recipe_details, name="recipe_details"),
]
