from django.db import models
from jsonfield import JSONField


class DateCreatedFieldObject(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class IngestedRecipe(DateCreatedFieldObject):
    content = JSONField() # for historical purposes, keep whatever was ingested
    url = models.URLField(null=True)

    DATA_SOURCES = (
        ('i', 'Internet'),
    )
    source = models.CharField(max_length=1, choices=DATA_SOURCES)


class Recipe(DateCreatedFieldObject):
    name = models.CharField(max_length=300)
    cooking_time_minutes = models.IntegerField()
    serve_min = models.IntegerField(null=True)
    serve_max = models.IntegerField(null=True)

    # TODO: add related names fields


class Ingredient(models.Model):
    name = models.CharField(max_length=200)


class RecipeIngredientItem(models.Model):
    recipe_id = models.ForeignKey(Recipe, related_name='ingredient_items', on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, related_name='ingredient_items', on_delete=models.CASCADE)
    # how much of this ingredient
    amount = models.FloatField()
    # what type of quantity (ex: cup? discrete amounts?)
    denomination = models.CharField(max_length=150)
    other_instructions = models.TextField()
    optional = models.BooleanField(default=False)


class RecipeStep(models.Model):
    recipe_id = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    step_number = models.IntegerField()
    instruction = models.TextField()
