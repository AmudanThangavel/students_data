# Generated by Django 4.0.6 on 2022-09-21 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='students_data',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]