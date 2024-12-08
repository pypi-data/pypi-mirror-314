# Generated by Django 5.1.2 on 2024-11-27 01:42

import django.db.models.deletion
import kitchenai.core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmbedObject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("text", models.CharField(max_length=255)),
                ("ingest_label", models.CharField(max_length=255)),
                ("status", models.CharField(default="pending", max_length=255)),
                ("metadata", models.JSONField(default=dict)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FileObject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "file",
                    models.FileField(
                        upload_to=kitchenai.core.models.file_object_directory_path
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("ingest_label", models.CharField(max_length=255)),
                ("status", models.CharField(default="pending", max_length=255)),
                ("metadata", models.JSONField(default=dict)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="KitchenAIManagement",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        default="kitchenai_management",
                        max_length=255,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("project_name", models.CharField(max_length=255)),
                ("version", models.CharField(max_length=255)),
                ("description", models.TextField(default="")),
                ("jupyter_token", models.CharField(default="", max_length=255)),
                ("jupyter_host", models.CharField(default="", max_length=255)),
                ("jupyter_port", models.CharField(default="8888", max_length=255)),
                ("jupyter_protocol", models.CharField(default="http", max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="KitchenAIDependencies",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "kitchen",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.kitchenaimanagement",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="KitchenAIModule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("jupyter_path", models.CharField(default="", max_length=255)),
                (
                    "file",
                    models.FileField(
                        upload_to=kitchenai.core.models.module_directory_path
                    ),
                ),
                (
                    "kitchen",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.kitchenaimanagement",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="KitchenAIPlugins",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "kitchen",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.kitchenaimanagement",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="KitchenAIRootModule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "kitchen",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.kitchenaimanagement",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
