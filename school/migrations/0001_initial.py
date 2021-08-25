# Generated by Django 3.2.4 on 2021-08-23 00:39

from django.db import migrations, models
import school.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, null=True, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=school.models.upload_logo)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]