# Generated by Django 2.0.7 on 2020-01-22 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIfitnesstrainer', '0008_auto_20200122_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='height',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='order',
            name='weight',
            field=models.CharField(max_length=11),
        ),
    ]
