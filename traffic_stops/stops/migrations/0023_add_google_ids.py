# Generated by Django 4.1 on 2023-12-14 19:54

import csv
from django.db import migrations
from traffic_stops.settings import data_dir
from stops.models import Agency

### START CONFIG ###
drive_id_path = data_dir + 'drive_log.csv'
### END CONFIG ###

def update_drive_ids(apps,schema_editor):
    drive_ids = csv.DictReader(open(drive_id_path))
    for row in drive_ids:
        agency = Agency.objects.get(name=row['name'])
        agency.public_drive_id = row['id']
        agency.save()



class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0022_fix_crete_normal'),
    ]

    operations = [
            migrations.RunPython(update_drive_ids)
    ]
