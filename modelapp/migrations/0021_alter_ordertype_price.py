# Generated by Django 4.2.2 on 2025-01-09 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelapp', '0020_rename_file_url_message_file_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertype',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
