# Generated by Django 3.1.2 on 2020-10-04 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrequest',
            name='request_type',
            field=models.CharField(choices=[('SIGN_IN', 'SIGN_IN'), ('ORDINARY', 'ORDINARY')], default='SIGN_IN', max_length=20),
        ),
    ]
