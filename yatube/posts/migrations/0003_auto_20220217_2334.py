# Generated by Django 2.2.19 on 2022-02-17 20:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0002_auto_20220217_2317"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="slug",
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="group",
            field=models.ForeignKey(
                blank=True,
                max_length=200,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to="posts.Group",
            ),
        ),
    ]
