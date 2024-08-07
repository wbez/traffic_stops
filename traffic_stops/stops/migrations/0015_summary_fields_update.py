# Generated by Django 4.1 on 2023-05-10 22:13

from django.db import migrations
from stops.models import Stop

### START CONFIG ###
fields_to_update = ['driver_race','search_conducted','search_hit',
        'consent_search_requested','consent_search_conducted',
        'dog_sniff','dog_search_conducted','dog_search_hit',
        'outcome']
interval = 200000
### END CONFIG ###


def summarize(apps,schema_editor):
    # query stops just to get the ids, hopefully memory efficient
    stops = Stop.objects.all()
    stop_ids = [x[0] for x in Stop.objects.values_list('id')]

    # a range of values to start with
    lower_range = 0
    upper_range = interval

    while lower_range < len(stop_ids):
        print('querying ids',lower_range,'-',upper_range)
        # get a slice of stops based on an interval slice of ids
        stop_id_q = stop_ids[lower_range:upper_range]
        stop_q = Stop.objects.filter(id__in=stop_id_q)

        print('updating')
        # updates
        for stop in stop_q:
            stop.driver_race = stop.get_driver_race()
            stop.search_conducted = stop.get_search_conducted()
            stop.search_hit = stop.get_search_hit()
            stop.consent_search_requested = stop.get_consent_search_requested()
            stop.consent_search_conducted = stop.get_consent_search_conducted()
            stop.dog_sniff = stop.get_dog_sniff()
            stop.dog_search_conducted = stop.get_dog_search_conducted()
            stop.dog_search_hit = stop.get_dog_search_hit()
            stop.outcome = stop.get_outcome()

        print('saving')
        # save
        Stop.objects.bulk_update(stop_q,fields_to_update)

        # increment
        lower_range = upper_range
        # can't exceed the total number of stops in range
        upper_range += interval if upper_range + interval <= len(stop_ids) else len(stop_ids)



class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0014_load_2022_cpd'),
    ]

    operations = [
            migrations.RunPython(summarize)
    ]
