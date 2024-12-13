# Generated by Django 5.1.3 on 2024-12-13 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("yearly_steps", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recommendations",
            name="provider",
        ),
        migrations.AddField(
            model_name="recommendations",
            name="provider",
            field=models.ManyToManyField(to="yearly_steps.providerinfo"),
        ),
    ]
