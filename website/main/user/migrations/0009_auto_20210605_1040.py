# Generated by Django 2.2 on 2021-06-05 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20210605_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orders',
            field=models.CharField(max_length=45),
        ),
    ]
