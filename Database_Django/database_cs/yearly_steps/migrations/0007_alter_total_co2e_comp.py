# Generated by Django 5.1.3 on 2024-11-28 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("yearly_steps", "0006_rename_companys_total_co2e_comp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="total_co2e",
            name="comp",
            field=models.IntegerField(),
        ),
    ]
