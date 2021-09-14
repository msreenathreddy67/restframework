from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User

RECIPE_CHOICES = (
    ('V', 'Veg'),
    ('NV', 'Non Veg'),
)


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=60)
    recipe_type = models.CharField(max_length=2, choices=RECIPE_CHOICES)
    ingredients = models.TextField()
    procedure = models.TextField()
    process = JSONField()
    recipe_image = models.ImageField(upload_to='images/')
    # created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # process_val = JSONField(default=list)

    def __str__(self):
        return f'({self.recipe_name},{self.recipe_type})'

    class Meta:
        db_table = 'Recipe'


