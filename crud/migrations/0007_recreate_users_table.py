from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0006_yearlevel_alter_sections_id_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            # Drop the existing users table
            "DROP TABLE IF EXISTS crud_users;",
            # No reverse SQL needed as we're recreating the table
            reverse_sql=""
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=55)),
                ('email', models.EmailField(max_length=55, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('student_number', models.CharField(max_length=55, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('class_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud.sections')),
                ('year_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud.yearlevel')),
            ],
        ),
    ] 