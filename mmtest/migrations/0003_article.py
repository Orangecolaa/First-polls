# Generated by Django 3.2.6 on 2021-10-20 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmtest', '0002_mymodel_place_restaurant_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('status', models.CharField(max_length=32)),
                ('pub_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
