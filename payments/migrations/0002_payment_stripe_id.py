# Generated by Django 4.2.7 on 2023-12-02 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='stripe_id'),
        ),
    ]
