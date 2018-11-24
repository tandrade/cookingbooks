from django.db import models

from menu_planner.ingestors import InternetIngestor


class DateCreatedFieldObject(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class IngestedRecipe(DateCreatedFieldObject):
    content = models.TextField() # for historical purposes, keep whatever was ingested
    DATA_SOURCES = (
        ('internet', 'i'),
    )
    source_type = models.CharField(max_length=1, choices=DATA_SOURCES)

    def parse_content(self):
        # children must implement this method
        raise NotImplementedError

    class Meta:
        abstract = True


class InternetRecipe(IngestedRecipe):
    source = models.URLField() # for now, only supporting urls

    def parse_content(self):
        return InternetIngestor().ingest(self.source)


class Recipe(DateCreatedFieldObject):
    name = models.CharField(max_length=300)
    cooking_time_minutes = models.IntegerField(null=True)
    serve_min = models.IntegerField(null=True)
    serve_max = models.IntegerField(null=True)

    # TODO: add related names fields


class Ingredient(models.Model):
    name = models.CharField(max_length=200)


class RecipeIngredientItem(models.Model):
    recipe_id = models.ForeignKey(Recipe, related_name='ingredient_items', on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, related_name='ingredient_items', on_delete=models.CASCADE)

    other_instructions = models.TextField(null=True)
    optional = models.BooleanField(default=False)

    # options for amounts
    TEASPOON = 'tsp'
    TABLESPOON = 'tbsp'
    GRAM = 'g'
    CUP = 'cup'
    QUART = 'qt'
    OUNCE = 'oz'
    POUND = 'lb'
    COUNT = 'ct'

    MEASUREMENT_AMOUNT_CHOICES = (
        (TEASPOON, 'teaspoon'),
        (TABLESPOON, 'tablespoon'),
        (GRAM, 'gram'),
        (CUP, 'cup'),
        (QUART, 'quart'),
        (OUNCE, 'ounce'),
        (POUND, 'pound'),
        (COUNT, 'ct'), 
    )

    # how much and what unit of measurement
    # defaults to 1 count (1 of the item)
    amount = models.FloatField(default=1.0)
    denomination = models.CharField(max_length=5, choices=MEASUREMENT_AMOUNT_CHOICES, default=COUNT)


class RecipeStep(models.Model):
    recipe_id = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    step_number = models.IntegerField()
    instruction = models.TextField()
