# Generated by Django 5.0 on 2024-07-16 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(blank=True, default='Unknown', max_length=100, null=True),
        ),
    ]