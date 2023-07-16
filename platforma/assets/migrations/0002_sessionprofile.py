# Generated by Django 4.2.2 on 2023-07-13 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('session_key', models.CharField(max_length=40, unique=True)),
                ('ip_address', models.CharField(max_length=20)),
                ('last_accessed', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
