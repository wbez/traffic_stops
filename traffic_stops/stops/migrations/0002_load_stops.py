# Generated by Django 4.1 on 2022-09-01 21:55

from django.db import migrations
from stops.models import Stop


### START CONFIG ###
path_to_data_file = ''

### END CONFIG ###

def load_data(apps,schema_editor):
    for row in data_file:
        Stop.objects.create(
                AgencyCode = "")

    pass


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0001_initial'),
    ]

    operations = [
            migrations.RunPython(load_data)
    ]
