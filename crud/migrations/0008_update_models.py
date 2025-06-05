from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0007_recreate_users_table'),
    ]

    operations = [
        # First, remove foreign key constraints
        migrations.RunSQL(
            "SET FOREIGN_KEY_CHECKS=0;",
            "SET FOREIGN_KEY_CHECKS=1;"
        ),
        
        # Update YearLevel model
        migrations.AlterModelOptions(
            name='yearlevel',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='yearlevel',
            name='name',
            field=models.CharField(
                choices=[
                    ('First Year', 'First Year'),
                    ('Second Year', 'Second Year'),
                    ('Third Year', 'Third Year'),
                    ('Fourth Year', 'Fourth Year')
                ],
                max_length=55,
                unique=True
            ),
        ),
        
        # Update Sections model
        migrations.AlterModelOptions(
            name='sections',
            options={
                'ordering': ['name'],
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections'
            },
        ),
        migrations.AlterField(
            model_name='sections',
            name='name',
            field=models.CharField(
                choices=[
                    ('BSIT-1A', 'BSIT-1A'), ('BSIT-1B', 'BSIT-1B'), ('BSIT-1C', 'BSIT-1C'),
                    ('BSIT-2A', 'BSIT-2A'), ('BSIT-2B', 'BSIT-2B'), ('BSIT-2C', 'BSIT-2C'),
                    ('BSIT-3A', 'BSIT-3A'), ('BSIT-3B', 'BSIT-3B'), ('BSIT-3C', 'BSIT-3C'),
                    ('BSIT-4A', 'BSIT-4A'), ('BSIT-4B', 'BSIT-4B'), ('BSIT-4C', 'BSIT-4C')
                ],
                max_length=55,
                unique=True
            ),
        ),
        
        # Update Users model
        migrations.AlterModelOptions(
            name='users',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'User',
                'verbose_name_plural': 'Users'
            },
        ),
        migrations.AlterField(
            model_name='users',
            name='year_level',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='users',
                to='crud.yearlevel'
            ),
        ),
        migrations.AlterField(
            model_name='users',
            name='class_section',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='users',
                to='crud.sections'
            ),
        ),
        
        # Re-enable foreign key checks
        migrations.RunSQL(
            "SET FOREIGN_KEY_CHECKS=1;",
            "SET FOREIGN_KEY_CHECKS=0;"
        ),
    ] 