# Generated by Django 4.2.2 on 2024-11-18 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelapp', '0007_alter_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_type',
            field=models.CharField(choices=[('text', 'Text'), ('photo', 'Photo'), ('file', 'File')], default='text', max_length=10),
        ),
    ]