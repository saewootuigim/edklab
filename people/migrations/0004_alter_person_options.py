# Generated by Django 5.0.6 on 2024-07-23 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_person_priority'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['priority', '-year_finish']},
        ),
    ]
