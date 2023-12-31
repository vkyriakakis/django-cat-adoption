# Generated by Django 4.2.5 on 2023-09-21 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('age', models.CharField(choices=[('K', 'Kitten'), ('Y', 'Young'), ('A', 'Adult'), ('S', 'Senior')], max_length=1)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('color', models.CharField(choices=[('BLK', 'Black'), ('CAL', 'Calico'), ('WHT', 'White'), ('BLU', 'Blue'), ('GRA', 'Gray'), ('ORA', 'Orange'), ('BRN', 'Brown')], max_length=3)),
                ('image', models.ImageField(upload_to='images/cats')),
                ('is_sterilized', models.BooleanField()),
                ('is_vaccinated', models.BooleanField()),
                ('is_house_trained', models.BooleanField()),
            ],
        ),
    ]
