# Generated by Django 4.2.7 on 2023-12-28 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_notificationcategory_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMobileToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=512, unique=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mobile_tokens', to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'user mobile token',
                'verbose_name_plural': 'user mobile tokens',
                'db_table': 'user_mobile_token',
            },
        ),
    ]
