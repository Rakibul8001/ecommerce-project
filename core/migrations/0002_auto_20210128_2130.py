# Generated by Django 3.0 on 2021-01-28 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('shirt', 'SHIRT'), ('sportweare', 'SPORT WEARE'), ('outweare', 'OUT WEARE')], max_length=10),
        ),
    ]
