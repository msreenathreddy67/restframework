from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import action
from recipe.models import Recipe
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import RecipeSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class RecipeApiView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = (IsAuthenticated,) #a0ffd5732799992bcb25b927932bb6093dcfcac3

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        print(request.user)
        recipes = Recipe.objects.all()
        ser_obj = RecipeSerializer(recipes, many=True)
        return Response(ser_obj.data)

    def put(self, request):
        if not request.data.get("recipe_id") or not request.data.get("name"):
            return Response({"message": "Not a valid request"}, status=status.HTTP_400_BAD_REQUEST)
        recipe_id = request.data["recipe_id"]
        name = request.data["name"]
        recipe_obj = Recipe.objects.get(id=recipe_id)
        recipe_obj.recipe_name = name
        recipe_obj.save()
        return Response({"message": "Successfully Updated"})

    def post(self, request):
        serializer_obj = RecipeSerializer(data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data)
        return Response({"message": serializer_obj.errors})


class UserApiView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"message": "Invalid Credentials"})
    
    def delete(self, request):
        Token.objects.get(user=request.user).delete()
        return Response({"message": "Logged Out Successfully"})


class RecipeViewset(viewsets.ViewSet):
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    @action(methods=["GET"], detail=False)
    def get_recipes(self, request):
        recipes = list(Recipe.objects.values("id", "recipe_name", "ingredients"))
        return Response(recipes)

    @action(methods=["GET"], detail=False)
    def get_recipe_by_name(self, request):
        recipes = list(Recipe.objects.filter(recipe_name=request.data.get("name")).values("id", "recipe_name", "ingredients"))
        return Response(recipes)

    @action(methods=["GET", "DELETE"], detail=False)
    def get_recipe_by_id(self, request):
        if request.method == "GET":
            recipes = list(Recipe.objects.filter(id=request.data.get("id")).values("id", "recipe_name", "ingredients"))
            return Response(recipes)
        else:
            Recipe.objects.get(id=request.data.get("id")).delete()
            return Response({"message": "Successfully Deleted"})
