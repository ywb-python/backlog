# Generated by Django 2.0.1 on 2021-03-07 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='listuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='listuser',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Token',
        ),
        migrations.DeleteModel(
            name='ListUser',
        ),
    ]
