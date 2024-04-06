# Generated by Django 5.0.3 on 2024-04-01 13:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post_id',
            field=models.ForeignKey(db_column='post_id', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]