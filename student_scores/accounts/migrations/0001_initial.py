# Generated by Django 4.1.1 on 2022-09-20 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='students_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('roll_no', models.CharField(max_length=10)),
                ('department', models.CharField(max_length=35)),
                ('score', models.DecimalField(decimal_places=3, max_digits=10)),
                ('team_no', models.IntegerField()),
            ],
        ),
    ]
