# Generated by Django 3.1.2 on 2020-11-28 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificacion',
            name='fecha_creacion',
        ),
    ]