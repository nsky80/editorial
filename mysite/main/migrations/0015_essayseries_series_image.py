# Generated by Django 2.2.3 on 2019-07-21 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20190722_0316'),
    ]

    operations = [
        migrations.AddField(
            model_name='essayseries',
            name='series_image',
            field=models.ImageField(blank=True, default='images/sample-1.jpg', null=True, upload_to='images/series/'),
        ),
    ]
