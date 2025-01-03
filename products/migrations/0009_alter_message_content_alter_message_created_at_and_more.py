# Generated by Django 5.1.4 on 2024-12-26 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_review_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
