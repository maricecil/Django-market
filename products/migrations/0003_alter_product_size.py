# Generated by Django 5.1.4 on 2024-12-24 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('FREE', 'FREE')], default='FREE', max_length=4, verbose_name='사이즈'),
        ),
    ]