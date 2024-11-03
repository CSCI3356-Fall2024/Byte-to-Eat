# Generated by Django 5.1.2 on 2024-11-03 18:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_picture', models.ImageField(blank=True, null=True, upload_to='campaign_pictures/')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('individual_points', models.IntegerField(default=0)),
                ('group_points', models.IntegerField(default=0)),
                ('campaign_type', models.CharField(choices=[('action', 'Action'), ('redeem', 'Redeem')], max_length=10)),
                ('campaign_id', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('major', models.CharField(blank=True, max_length=100, null=True)),
                ('school', models.CharField(blank=True, max_length=100, null=True)),
                ('graduation_year', models.IntegerField(blank=True, null=True)),
                ('eagle_id', models.CharField(blank=True, max_length=20, null=True)),
                ('user_type', models.CharField(choices=[('student', 'Student'), ('mod', 'Moderator'), ('admin', 'Admin')], default='student', max_length=10)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('group_id', models.IntegerField(blank=True, null=True)),
                ('lifetime_points', models.IntegerField(default=0)),
                ('current_points', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=20, unique=True)),
                ('transaction_type', models.CharField(choices=[('action', 'Action'), ('redeem', 'Redeem')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.campaign')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
