# Generated by Django 4.0.4 on 2022-06-30 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wisapp', '0007_alter_schoolbalanceadd_options_sell'),
    ]

    operations = [
        migrations.AddField(
            model_name='fine',
            name='fine_descr',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
