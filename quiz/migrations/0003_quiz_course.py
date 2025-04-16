# Generated by Django 5.0.2 on 2024-02-27 12:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
        ('quiz', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='course.course'),
            preserve_default=False,
        ),
    ]
