# Generated by Django 3.0.8 on 2020-08-11 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control_panel', '0010_auto_20200811_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('used', models.BooleanField(default=False)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='control_panel.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_panel.Product')),
            ],
        ),
    ]
