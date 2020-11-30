# Generated by Django 3.1.2 on 2020-11-30 06:05

import api.managers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('bod', models.DateField()),
                ('dni', models.IntegerField(unique=True)),
                ('latitude', models.DecimalField(decimal_places=15, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=15, max_digits=20)),
                ('expo_token', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino')], default='F', max_length=9)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', api.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ACDiabetes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('glucemia_matutina', models.BooleanField(null=True)),
                ('opcional_glucemia_matutina', models.DecimalField(blank=True, decimal_places=2, max_digits=5)),
                ('glucemia_post_comida_principal', models.BooleanField(null=True)),
                ('opcional_glucemia_comida_principal', models.DecimalField(blank=True, decimal_places=2, max_digits=5)),
                ('fecha_hora_registro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ECNT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('imagen', models.ImageField(upload_to='')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ultimo_autocontrol', models.DateTimeField()),
                ('ecnts', models.ManyToManyField(blank=True, related_name='paciente_list', to='api.ECNT')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='paciente_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfesionalDeSalud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pacientes', models.ManyToManyField(blank=True, related_name='paciente_list', to='api.Paciente')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profesional_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AlertaACDiabetes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detalles', models.CharField(max_length=1024)),
                ('autocontrol_diabetes', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='alerta', to='api.acdiabetes')),
            ],
        ),
        migrations.CreateModel(
            name='ACDiabetesOpcional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aumento_fatiga', models.BooleanField(blank=True)),
                ('perdida_memoria', models.BooleanField(blank=True)),
                ('cambio_orina', models.BooleanField(blank=True)),
                ('perdida_vision', models.BooleanField(blank=True)),
                ('autocontrol_diabetes', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='autocontrol_opcional', to='api.acdiabetes')),
            ],
        ),
        migrations.AddField(
            model_name='acdiabetes',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autocontrol_diabetes', to='api.paciente'),
        ),
    ]
