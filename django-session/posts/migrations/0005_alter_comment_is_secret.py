# Generated by Django 5.0.3 on 2024-03-31 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_comment_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_secret',
            field=models.BooleanField(default=False, verbose_name='비밀댓글'),
        ),
    ]
