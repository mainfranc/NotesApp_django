# Generated by Django 3.2 on 2021-04-16 15:20

from django.db import migrations, models
import django.db.models.deletion
import organizer.models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0002_auto_20210409_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='task_date_time',
            field=models.DateTimeField(default=organizer.models._set_date),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=255)),
                ('rating', models.IntegerField(default=0)),
                ('note_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizer.note', verbose_name='Related Note')),
            ],
        ),
    ]
