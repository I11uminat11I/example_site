# Generated by Django 3.2.3 on 2021-08-15 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210611_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_breaking',
            field=models.BooleanField(default=False),
        ),
    ]
