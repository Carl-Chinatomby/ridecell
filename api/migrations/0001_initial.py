# Generated by Django 3.0.4 on 2020-03-25 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scooter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('is_reserved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance_traveled', models.DecimalField(decimal_places=6, max_digits=9)),
                ('payment_rate', models.DecimalField(decimal_places=2, max_digits=9)),
                ('scooter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Scooter')),
            ],
        ),
    ]
