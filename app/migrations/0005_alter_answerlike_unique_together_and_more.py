# Generated by Django 5.0 on 2024-11-08 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_answer_date_alter_question_date'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answerlike',
            unique_together={('profile', 'like')},
        ),
        migrations.AlterUniqueTogether(
            name='questionlike',
            unique_together={('profile', 'like')},
        ),
    ]