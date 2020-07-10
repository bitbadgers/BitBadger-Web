# Generated by Django 3.0.6 on 2020-06-20 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DevsPlatform', '0013_auto_20200620_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='max_number',
            field=models.IntegerField(default=20, verbose_name='Maximum number'),
        ),
        migrations.AlterField(
            model_name='team',
            name='goal',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Team Goal'),
        ),
    ]
