from django.db import migrations
from stops.models import Stop, Agency
import os, csv, datetime, dateparser, ipdb
from traffic_stops.settings import BASE_DIR, LOADER_DEBUG
from stops.utils.loaders import convert_date, convert_time_ampm, \
        convert_int, convert_duration, get_year, \
        make_record_ref, get_max_stop_id
from stops.models import Stop, Agency

### START CONFIG ###
data_dir = str(BASE_DIR) + '/data/'
data_filenames = [
                  '2022_ITSS.txt'
                  ]
agency_lookup_filepath = data_dir + 'agency_codes_2022.csv' 
### END CONFIG ###

def init(apps, schema_editor):
    load_files()
    create_new_agencies()
    update_stop_agencies()


def build_agency_lookup():
    # set up agency code lookup
    agency_codes = {}
    agency_code_csv = [x for x in csv.DictReader(open(agency_lookup_filepath))]
    for agency in agency_code_csv:
        agency_codes[agency['code']] = agency['name']
    return agency_codes


def load_files():
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


def update_stop_agencies():
    """
    for each agency
    look up their stops
    and update the related agency
    """
    for agency in Agency.objects.all():
        stops = Stop.objects.filter(AgencyCode=agency.code,agency=None)
        stops.update(agency=agency,AgencyName=agency.name)
        stops.save()
        print('updated',agency.name,'stops')


def create_new_agencies():
    """
    create agencies 
    that don't already exist
    """
    agencies = build_agency_lookup()
    for agency_code in agencies:
        agency, created = Agency.objects.get_or_create(code=agency_code)
        if created:
            agency_name = agencies[agency_code]
            agency.name = agency_name
            agency.save()
            print('created agency',agency.__dict__)


def load_data(data_csv,year):
    # keep track of each stop
    stop_objs = []
    counter = 1

    # roll thru data
    for row in data_csv:
        row_date = row['DateOfStop'].split()[0]
        row_date_formatted = convert_date(row_date)
        row_time = row['TimeOfStop']
        row_time_formatted = convert_time_ampm(row_time,counter)
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
        print(counter)
        if LOADER_DEBUG:
            if counter > 10:
                break
    
    Stop.objects.bulk_create(stop_objs)


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0012_add_census_data'),
    ]

    operations = [
            migrations.RunPython(init)
    ]
