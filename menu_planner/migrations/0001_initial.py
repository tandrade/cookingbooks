# Generated by Django 2.0.4 on 2018-05-07 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='InternetRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('source_type', models.CharField(choices=[('internet', 'i')], max_length=1)),
                ('source', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=300)),
                ('cooking_time_minutes', models.IntegerField()),
                ('serve_min', models.IntegerField(null=True)),
                ('serve_max', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredientItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('denomination', models.CharField(max_length=150)),
                ('other_instructions', models.TextField()),
                ('optional', models.BooleanField(default=False)),
                ('ingredient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_items', to='menu_planner.Ingredient')),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_items', to='menu_planner.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.IntegerField()),
                ('instruction', models.TextField()),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='menu_planner.Recipe')),
            ],
        ),
    ]