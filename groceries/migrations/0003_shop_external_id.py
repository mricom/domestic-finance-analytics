# Generated by Django 5.0 on 2024-08-07 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries', '0002_alter_invoiceline_purchase_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='external_id',
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]