# Generated by Django 3.2.6 on 2022-12-08 03:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('accion', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('metadatos', models.JSONField()),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autor_log', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'log',
                'managed': True,
            },
        ),
    ]
