# Generated by Django 4.0.4 on 2022-06-30 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wisapp', '0008_fine_fine_descr'),
    ]

    operations = [
        migrations.AddField(
            model_name='finehistory',
            name='fine_descr',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
