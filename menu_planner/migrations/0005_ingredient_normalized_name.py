# Generated by Django 2.0.4 on 2018-12-29 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_planner', '0004_auto_20181122_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='normalized_name',
            field=models.CharField(default='ingredient', max_length=200),
            preserve_default=False,
        ),
    ]
