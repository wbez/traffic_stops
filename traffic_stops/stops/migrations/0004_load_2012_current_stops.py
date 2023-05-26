from django.db import migrations
from stops.models import Stop
import os, csv, datetime, dateparser, ipdb
from traffic_stops.settings import BASE_DIR, LOADER_DEBUG
from stops.utils.loaders import convert_date, convert_time, \
        convert_int, convert_duration, get_year, \
        make_record_ref, get_max_stop_id

### START CONFIG ###
data_dir = str(BASE_DIR) + '/data/'
data_filenames = [
                  '2012 ITSS Data.txt',
                  '2013 ITSS Data.txt',
                  '2014 ITSS Data.txt',
                  '2015 ITSS Data.txt',
                  '2016 ITSS Data.txt',
                  '2017 ITSS Data.txt',
                  '2018 ITSS Data.txt',
                  '2019_ITSS_Statewide_Redacted.txt',
                  '2020 Traffic Data Redacted.txt',
                  '2021 Traffic Data Redacted.txt'
                  ]
### END CONFIG ###


def load_files(apps,schema_editor):
    # load each file one at a time
    for filename in data_filenames:
        print('loading',filename)
        file_path = data_dir + filename 
        year = filename[0:4]
        # convert to csv
        data_file = open(file_path,encoding='latin-1') #TODO verify this encoding
        data_csv = csv.DictReader(data_file,delimiter='~')
        try:
            load_data(data_csv,year)
        except Exception as e:
            print(e)
            import ipdb; ipdb.set_trace()


def load_data(data_csv,year):
    # keep track of each stop
    stop_objs = []
    counter = 1
    next_stop_id = get_max_stop_id() + 1
    
    # handle inconsistent field names
    agency_row_name = 'AgencyName' if 'AgencyName' in data_csv.fieldnames else 'Agency Name'
    
    #header_assignments = header_assignments()

    for row in data_csv:
        row_date = row['DateOfStop'][0:10]
        row_date_formatted = convert_date(row_date)
        row_time = row['TimeOfStop'].strip()[0:5]
        # cleanup to handle imprecise slicing (hours can be single digits)
        if row_time[-1] == ':':
            row_time = row_time[:-1]
        row_time_formatted = convert_time(row_time,counter)
        row_duration = row['DurationOfStop']
        row_duration_formatted = convert_duration(row_duration)
        
        # cleanup
        for key in row:
            if row[key] in ('#REF!',''):
                row[key] = None
            # convert ints to int or none
            if key in ['VehicleYear']:
                row[key] = convert_int(row[key],counter)

        try:
            stop_obj = Stop(
                        year = year,
                        record_ref = make_record_ref(year,counter),
                        AgencyCode = row['AgencyCode'],
                        AgencyName = row[agency_row_name],
                        DateOfStop = row_date_formatted,
                        TimeOfStop = row_time_formatted,
                        DurationOfStop = row_duration_formatted,
                        ZIP = row['ZIP'],
                        VehicleMake = row['VehicleMake'],
                        VehicleYear = row['VehicleYear'],
                        DriversYearofBirth = row['DriversYearofBirth'],
                        DriverSex = row['DriverSex'],
                        DriverRace = row['DriverRace'],
                        ReasonForStop = row['ReasonForStop'],
                        TypeOfMovingViolation = row['TypeOfMovingViolation'],
                        ResultOfStop = row['ResultOfStop'],
                        BeatLocationOfStop = row['BeatLocationOfStop'],
                        VehicleConsentSearchRequested = row['VehicleConsentSearchRequested'],
                        VehicleConsentGiven = row['VehicleConsentGiven'],
                        VehicleSearchConducted = row['VehicleSearchConducted'],
                        VehicleSearchConductedBy = row['VehicleSearchConductedBy'],
                        VehicleContrabandFound = row['VehicleContrabandFound'],
                        VehicleDrugsFound = row['VehicleDrugsFound'],
                        VehicleDrugParaphernaliaFound = row['VehicleDrugParaphernaliaFound'],
                        VehicleAlcoholFound = row['VehicleAlcoholFound'],
                        VehicleWeaponFound = row['VehicleWeaponFound'],
                        VehicleStolenPropertyFound = row['VehicleStolenPropertyFound'],
                        VehicleOtherContrabandFound = row['VehicleOtherContrabandFound'],
                        VehicleDrugAmount = row['VehicleDrugAmount'],
                        DriverConsentSearchRequested = row['DriverConsentSearchRequested'],
                        DriverConsentGiven = row['DriverConsentGiven'],
                        DriverSearchConducted = row['DriverSearchConducted'],
                        DriverSearchConductedBy = row['DriverSearchConductedBy'],
                        PassengerConsentSearchRequested = row['PassengerConsentSearchRequested'],
                        PassengerConsentGiven = row['PassengerConsentGiven'],
                        PassengerSearchConducted = row['PassengerSearchConducted'],
                        PassengerSearchConductedBy = row['PassengerSearchConductedBy'],
                        DriverPassengerContrabandFound = row['DriverPassengerContrabandFound'],
                        DriverPassengerDrugsFound = row['DriverPassengerDrugsFound'],
                        DriverPassengerDrugParaphernaliaFound = row['DriverPassengerDrugParaphernaliaFound'],
                        DriverPassengerAlcoholFound = row['DriverPassengerAlcoholFound'],
                        DriverPassengerWeaponFound = row['DriverPassengerWeaponFound'],
                        DriverPassengerStolenPropertyFound = row['DriverPassengerStolenPropertyFound'],
                        DriverPassengerOtherContrabandFound = row['DriverPassengerOtherContrabandFound'],
                        DriverPassengerDrugAmount = row['DriverPassengerDrugAmount'],
                        PoliceDogPerformSniffOfVehicle = row['PoliceDogPerformSniffOfVehicle'],
                        PoliceDogAlertIfSniffed = row['PoliceDogAlertIfSniffed'],
                        PoliceDogVehicleSearched = row['PoliceDogVehicleSearched'],
                        PoliceDogContrabandFound = row['PoliceDogContrabandFound'],
                        PoliceDogDrugsFound = row['PoliceDogDrugsFound'],
                        PoliceDogDrugParaphernaliaFound = row['PoliceDogDrugParaphernaliaFound'],
                        PoliceDogAlcoholFound = row['PoliceDogAlcoholFound'],
                        PoliceDogWeaponFound = row['PoliceDogWeaponFound'],
                        PoliceDogStolenPropertyFound = row['PoliceDogStolenPropertyFound'],
                        PoliceDogOtherContrabandFound = row['PoliceDogOtherContrabandFound'],
                        PoliceDogDrugAmount = row['PoliceDogDrugAmount']
                )
            stop_objs.append(stop_obj)

        except Exception as e:
            print('counter:',counter)
            print('error:',e)
            ipdb.set_trace()

        counter += 1
        next_stop_id += 1
        if LOADER_DEBUG:
            if counter > 10:
                break

    
    Stop.objects.bulk_create(stop_objs)


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0003_load_2007_2011_stops'),
    ]

    operations = [
            migrations.RunPython(load_files)
    ]
