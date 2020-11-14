# Generated by Django 3.1.3 on 2020-11-14 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20201113_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfesionalDeSalud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pacientes', models.ManyToManyField(blank=True, related_name='paciente_list', to='api.Paciente')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profesional_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
