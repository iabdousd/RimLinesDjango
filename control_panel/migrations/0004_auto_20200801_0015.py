# Generated by Django 3.0.8 on 2020-08-01 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_panel', '0003_auto_20200731_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(auto_created=True, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
    ]
