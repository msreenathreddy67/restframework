from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Recipe
from .form import RecipeForm, ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def user_form(request):
    return render(request, 'recipe/userform.html')


def saveuser(request):
    if request.method == 'POST':
        print("-------->", request.POST)
        print("username ------>", request.POST['username'])
        print("first_name ---->", request.POST['first_name'])
        print("last_name ------>", request.POST['last_name'])
        print("email ------>", request.POST['email'])
        print("password ------>", request.POST['password'])
        user = User.objects.create_user(username=request.POST['username'],
                                        first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        email=request.POST['email'],
                                        password=request.POST['password'])
        user.save()
        return render(request, 'recipe/login.html', {'msg':'User is saved Successfully ....!'} )


def login_form(request):
    return render(request, 'recipe/login.html')


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        name = ""#query
        org = ""#query
        request.session["org"] = org
        request.session["name"] = name
        return HttpResponseRedirect("/app/")
    else:
        return HttpResponse("Invalid Credentials")


def logout_view(request):
    request.session.clear()
    request.session.delete()
    logout(request)
    return HttpResponseRedirect("/app/login_form/")

def register_recipe(request):
    org = request.session["org"]
    name = request.session["name"]
    form = RecipeForm()
    return render(request, 'recipe/recipe_form.html', {"form": form})

@login_required(login_url="/app/login_form/")
def saverecepi(request):
    if request.method == 'POST':
        # recipe_form = RecipeForm(request.POST)
        # if recipe_form.is_valid():
        #     recipe_obj = recipe_form.save(commit=False)
        #     recipe_obj.created_by = request.user
        #     recipe_obj.save()
        #     return HttpResponseRedirect("/app/")
        # else:
        #     return render(request, 'recipe/recipe_form.html', {"errors": recipe_form.errors, "form": RecipeForm()})
        import pdb; pdb.set_trace()
        if request.POST.get("recipe_name") and request.POST.get("recipe_type"):
            recipe = Recipe(recipe_name=request.POST['recipe_name'],
                            recipe_type=request.POST['recipe_type'],
                            ingredients=request.POST['ingredients'],
                            procedure=request.POST['procedure'],
                            recipe_image=request.FILES["recipe_image"])
            recipe.save()
        else:
            if not request.POST.get("recipe_name"):
                msg = "Recipe Name is missing"
            elif not request.POST.get("recipe_type"):
                msg = "Recipe Ingredients are missing"
            return render(request, 'recipe/recipe_form.html', {'msg': msg, "form": RecipeForm()} )
    return render(request, 'recipe/recipe_form.html', {'msg': 'Recipe is saved Successfully ....!', "form": RecipeForm()} )

@login_required(login_url="/app/login_form/")
def recipe_booklet(request):
    recipe_list = Recipe.objects.all()
    return render(request, 'recipe/recipe.html', {'recipe_list': recipe_list})

@login_required(login_url="/app/login_form/")
def deleterecipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipes = Recipe.objects.all()
    print('Recipe-------->', recipe)
    recipe.delete()
    return render(request, 'recipe/recipe.html', {'msg': 'The recipe Deleted Successfully ...!',
                                                  'recipe_list': recipes})

@login_required(login_url="/app/login_form/")
def editrecipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe/recipe_form.html', {"recipe": recipe} )


def contact_form(request):
    if request.method == "GET":
        return render(request, "recipe/contact_form.html", { "recipe_form": RecipeForm(), "form": ContactForm()})
    else:
        form = ContactForm(request.POST)
        recipe_form = RecipeForm(request.POST)
        if form.is_valid() and recipe_form.is_valid():
            recipe_form.save()
            ## email sending functionality
            cc_myself = form.cleaned_data["cc_myself"]
            return render(request, "recipe/contact_form.html", { "recipe_form": RecipeForm(),"form": ContactForm()})
        else:
            return render(request, "recipe/contact_form.html", {"form": ContactForm(), "recipe_form": RecipeForm(), "errors": form.errors})


def recipe_details(request, recipe_id):
    recipe_obj = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipe/details.html', {"recipe": recipe_obj})
