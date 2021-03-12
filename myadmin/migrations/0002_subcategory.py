# Generated by Django 3.1.4 on 2021-01-10 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('SubCategory_ID', models.AutoField(primary_key=True, serialize=False)),
                ('SubCategory_name', models.CharField(max_length=30, unique=True)),
                ('SubCategory_file', models.CharField(max_length=100)),
            ],
        ),
    ]