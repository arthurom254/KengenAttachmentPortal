# Generated by Django 4.2.1 on 2023-06-26 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Kengen', '0002_logs_comments_delete_hr_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='student_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Kengen.student'),
        ),
    ]