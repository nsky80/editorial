# Generated by Django 2.2.3 on 2019-07-21 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_delete_hotel'),
    ]

    operations = [
        migrations.AddField(
            model_name='essaycategory',
            name='essay_image',
            field=models.ImageField(blank=True, default='images/sample-1.jpg', null=True, upload_to='images/category/'),
        ),
    ]
