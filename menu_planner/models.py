from django.db import models
from jsonfield import JSONField


class DateCreatedFieldObject(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

# for historical purposes, keep whatever was ingested
class IngestedRecipe(DateCreatedFieldObject):
    ingested = JSONField()
    url = models.URLField(null=True)

    DATA_SOURCES = (
        ('i', 'Internet'),
    )
    source = models.CharField(max_length=1, choices=DATA_SOURCES)


class Recipe(DateCreatedFieldObject):
    name = models.CharField(max_length=300)
    cooking_time_minutes = modes.IntegerField()
    serve_min = models.IntegerField(required=False)
    serve_max = models.IntegerField(required=False)

class Ingredient(models.Model):
    name = models.CharField(max_length=200)

class RecipeIngredientItem(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.Cascade)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.Cascade)
    # how much of this ingredient
    amount = models.FloatField()
    # what type of quantity (ex: cup? discrete amounts?)
    denomination = models.CharField(max_length=150)
    other_instructions = models.TextField()
    optional = models.Boolean(default=False)

class RecipeStep(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.Cascade)
    step_number = models.IntegerField()
    instruction = models.TextField()
