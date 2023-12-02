# Generated by Django 4.2.7 on 2023-12-01 03:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('photo_booths', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=128, null=True)),
            ],
            options={
                'verbose_name': 'concept',
                'verbose_name_plural': 'concepts',
                'db_table': 'concept',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('frame_color', models.CharField(max_length=8)),
                ('participants', models.IntegerField()),
                ('camera_shot', models.CharField(max_length=8)),
                ('goods_amount', models.BooleanField(null=True)),
                ('curl_amount', models.BooleanField(null=True)),
                ('is_public', models.BooleanField(default=False)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('concepts', models.ManyToManyField(related_name='reviews', to='reviews.concept')),
                ('photo_booth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='photo_booths.photobooth')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
                'db_table': 'review',
            },
        ),
        migrations.CreateModel(
            name='UserReviewLikeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'user review like log',
                'verbose_name_plural': 'user review like logs',
                'db_table': 'user_review_like_log',
            },
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_image_url', models.URLField()),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_images', to='reviews.review')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'review image',
                'verbose_name_plural': 'review images',
                'db_table': 'review_image',
            },
        ),
        migrations.AddField(
            model_name='review',
            name='user_review_like_logs',
            field=models.ManyToManyField(related_name='review_like_logs', through='reviews.UserReviewLikeLog', to=settings.AUTH_USER_MODEL),
        ),
    ]
