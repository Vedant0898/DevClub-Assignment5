# Generated by Django 4.0.6 on 2022-07-13 11:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_alter_instructor_verification_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instructor',
            options={'ordering': ['first_name', 'last_name']},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['first_name', 'last_name']},
        ),
        migrations.AddField(
            model_name='instructor',
            name='about',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='instructor',
            name='date_joined',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructor',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructor',
            name='first_name',
            field=models.CharField(default='dummy First name', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructor',
            name='last_name',
            field=models.CharField(default='Dummy last name', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='about',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='date_joined',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(default='dummy first name', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(default='dummy last name', max_length=30),
            preserve_default=False,
        ),
    ]
