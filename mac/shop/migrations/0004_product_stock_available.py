# Generated by Django 4.1.5 on 2023-01-13 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_available',
            field=models.CharField(default='', max_length=50),
        ),
    ]