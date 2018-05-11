from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender='menu_planner.InternetRecipe')
def convert_ingested_recipe(sender, **kwargs):
    return InternetParser().parse(**kwargs['content'])
