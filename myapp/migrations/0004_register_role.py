# Generated by Django 3.1.4 on 2021-01-04 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210104_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='role',
            field=models.CharField(default='user', max_length=20),
            preserve_default=False,
        ),
    ]