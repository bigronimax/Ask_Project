# Generated by Django 5.0 on 2024-11-11 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_answerlike_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerlike',
            name='like',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='questionlike',
            name='like',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]