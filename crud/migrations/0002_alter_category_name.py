# Generated by Django 4.2.8 on 2025-06-08 07:06

from django.db import migrations, models

def add_categories(apps, schema_editor):
    Category = apps.get_model('crud', 'Category')
    categories = ['Bullying', 'Cheating', 'Teacher Abuse', 'Others']
    for category in categories:
        Category.objects.get_or_create(name=category)

class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Bullying', 'Bullying'), ('Cheating', 'Cheating'), ('Teacher Abuse', 'Teacher Abuse'), ('Others', 'Others')], max_length=55, unique=True),
        ),
        migrations.RunPython(add_categories),
    ]
