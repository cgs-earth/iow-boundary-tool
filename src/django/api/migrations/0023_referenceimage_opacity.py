# Generated by Django 3.2.13 on 2022-10-24 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_alter_user_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='referenceimage',
            name='opacity',
            field=models.PositiveSmallIntegerField(default=100),
        ),
    ]
