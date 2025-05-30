# Generated by Django 5.0.4 on 2024-12-02 14:53

import django.db.models.deletion
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_comment_created_alter_comment_modified_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='عنوان')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('active', models.BooleanField(default=False, verbose_name='وضعیت')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.post', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': ' تصویر ها',
                'ordering': ['-created'],
                'indexes': [models.Index(fields=['created'], name='blog_image_created_1ba45b_idx')],
            },
        ),
    ]
