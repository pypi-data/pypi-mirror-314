# Generated by Django 5.1.2 on 2024-12-01 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_codeimport_label_codesetup_label"),
    ]

    operations = [
        migrations.AlterField(
            model_name="codeimport",
            name="label",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="codesetup",
            name="label",
            field=models.CharField(max_length=255),
        ),
    ]
