# Generated by Django 3.0.8 on 2020-08-03 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_panel', '0008_auto_20200803_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(null=True),
        ),
    ]