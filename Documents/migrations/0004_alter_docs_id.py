# Generated by Django 4.0.6 on 2022-07-28 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Documents', '0003_alter_docs_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docs',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
