# Generated by Django 4.2.5 on 2023-10-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopt', '0002_remove_adoptionrequest_is_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adoptionrequest',
            name='reason',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
