# Generated by Django 3.2.3 on 2021-10-14 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_visitors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visitors',
            field=models.JSONField(default=None, null=True),
        ),
    ]