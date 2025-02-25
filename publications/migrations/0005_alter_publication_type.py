# Generated by Django 5.0.6 on 2024-07-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0004_alter_publication_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='type',
            field=models.CharField(choices=[('Article', 'Article'), ('Review', 'Review'), ('Protocol', 'Protocol'), ('Patent', 'Patent'), ('Dissertation', 'Dissertation')], default='Journal', max_length=13),
        ),
    ]
