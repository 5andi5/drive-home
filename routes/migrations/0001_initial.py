# Generated by Django 3.1.2 on 2020-10-29 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_point', models.CharField(max_length=255)),
                ('end_point', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutes', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routes.route')),
            ],
        ),
    ]