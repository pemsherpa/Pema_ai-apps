# Generated by Django 5.1.4 on 2025-01-20 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("yearly_steps", "0002_plans_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="providers",
            name="phone_number",
            field=models.CharField(max_length=255),
        ),
    ]
