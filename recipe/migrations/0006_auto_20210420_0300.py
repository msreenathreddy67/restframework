# Generated by Django 3.0.8 on 2021-04-20 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_recipe_process_val'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='process_val',
        ),
        migrations.AddField(
            model_name='recipe',
            name='recipe_image',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
    ]
