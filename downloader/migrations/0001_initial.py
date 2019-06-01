# Generated by Django 2.2.1 on 2019-05-27 10:32

from django.db import migrations, models
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_set', models.CharField(max_length=128)),
                ('attributes', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('json_content', jsonfield.fields.JSONField()),
                ('status', models.CharField(default='pending', max_length=16)),
                ('data_set', models.TextField(default='???', max_length=128)),
                ('msg', models.CharField(max_length=512)),
            ],
        ),
    ]