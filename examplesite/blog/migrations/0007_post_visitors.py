# Generated by Django 3.2.3 on 2021-10-14 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visitors',
            field=models.JSONField(null=True),
        ),
    ]
