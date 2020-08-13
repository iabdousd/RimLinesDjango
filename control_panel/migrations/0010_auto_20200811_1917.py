# Generated by Django 3.0.8 on 2020-08-11 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control_panel', '0009_auto_20200803_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionCredentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_created=True)),
                ('phone_number', models.CharField(max_length=200, null=True)),
                ('from_destination', models.CharField(max_length=200, null=True)),
                ('amount', models.FloatField()),
                ('method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='control_panel.PaymentMethod')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_created=True)),
                ('verified', models.BooleanField(default=False)),
                ('credentials', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='control_panel.TransactionCredentials')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='Transaction',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='control_panel.Transaction'),
        ),
    ]
