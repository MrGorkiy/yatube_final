# Generated by Django 2.2.16 on 2022-04-20 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20220418_2248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Подписку', 'verbose_name_plural': 'Подписки'},
        ),
    ]