from rest_framework import serializers
from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        # fields = ["recipe_name", "recipe_type", "ingredients", "process"]
        fields = '__all__'

