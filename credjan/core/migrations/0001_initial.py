# Generated by Django 4.1.7 on 2023-06-24 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PERSON',
            fields=[
                ('id', models.IntegerField(default=None, primary_key=True, serialize=False)),
                ('Name', models.CharField(default=None, max_length=32)),
                ('Surname', models.CharField(default=None, max_length=32)),
                ('BirthDate', models.DateField(default=None, max_length=30)),
                ('Sex', models.CharField(default=None, max_length=1)),
            ],
        ),
    ]
