# Generated by Django 3.2.6 on 2022-12-20 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0003_alumnoseccion_docenteseccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='seccion',
            name='agno',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seccion',
            name='semestre',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
