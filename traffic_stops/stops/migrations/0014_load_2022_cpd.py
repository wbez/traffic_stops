from django.db import migrations
from stops.models import Stop, Agency
import os, csv, datetime, dateparser, ipdb
from traffic_stops.settings import BASE_DIR, LOADER_DEBUG
from stops.utils.loaders import convert_date, convert_time, \
        convert_int, convert_duration, get_year, \
        get_max_stop_id, make_record_ref
from django.db import connection


### START CONFIG ###
data_dir = str(BASE_DIR) + '/data/'
data_filenames = [
                '2022_ITSS_CPD.csv'
                  ]
agency_code = '13194'
agency_name = 'CHICAGO POLICE'
### END CONFIG ###


def load_files(apps,schema_editor):
    # load each file one at a time
    for filename in data_filenames:
        print('loading',filename)
        file_path = data_dir + filename 
        year = filename[0:4]
        # convert to csv
        data_file = open(file_path,encoding='latin-1') #TODO verify this encoding
        data_csv = csv.DictReader(data_file)
        try:
            load_data(data_csv,year)
        except Exception as e:
            print(e)
            import ipdb; ipdb.set_trace()


def load_data(data_csv,year):
    # keep track of each stop
    stop_objs = []
    counter = 0
    cpd = Agency.objects.get(code=agency_code)

    for row in data_csv:
        counter += 1
        row_date = row['DATESTOP'][0:10]
        row_date_formatted = convert_date(row_date)
        row_time = row['TIMESTOP'].strip()[0:5]
        # cleanup to handle imprecise slicing (hours can be single digits)
        if row_time[-1] == ':':
            row_time = row_time[:-1]
        row_time_formatted = convert_time(row_time,counter)
        row_duration = row['DURATION']
        row_duration_formatted = convert_duration(row_duration)
        
        # cleanup
        for key in row:
            if row[key] in ('#REF!',''):
                row[key] = None
            # convert ints to int or none
            if key in ['VEHYEAR']:
                row[key] = convert_int(row[key],counter)


        try:
            stop_obj = Stop(
                        AgencyCode = agency_code,
                        AgencyName = agency_name,
                        agency = cpd,
                        year = year,
                        DateOfStop = row_date_formatted,
                        TimeOfStop = row_time_formatted,
                        DurationOfStop = row_duration_formatted,
                        ZIP = row['ZIPCODE'],
                        VehicleMake = row['VEHMAKE'],
                        VehicleYear = row['VEHYEAR'],
                        DriversYearofBirth = row['YRBIRTH'],
                        DriverSex = row['DRSEX'],
                        DriverRace = row['DRRACE'],
                        ReasonForStop = row['REASSTOP'],
                        TypeOfMovingViolation = row['TYPEMOV'],
                        ResultOfStop = row['RESSTOP'],
                        BeatLocationOfStop = row['BEAT_I'],
                        VehicleConsentSearchRequested = row['VEHCONSREQ'],
                        VehicleConsentGiven = row['VEHCONSGIV'],
                        VehicleSearchConducted = row['VEHSRCHCOND'],
                        VehicleSearchConductedBy = row['VEHSRCHCONDBY'],
                        VehicleContrabandFound = row['VEHCONTRA'],
                        VehicleDrugsFound = row['VEHDRUGS'],
                        VehicleDrugParaphernaliaFound = row['VEHPARA'],
                        VehicleAlcoholFound = row['VEHALC'],
                        VehicleWeaponFound = row['VEHWEAP'],
                        VehicleStolenPropertyFound = row['VEHSTOLPROP'],
                        VehicleOtherContrabandFound = row['VEHOTHER'],
                        VehicleDrugAmount = row['VEHDRAMT'],
                        DriverConsentSearchRequested = row['DRCONSREQ'],
                        DriverConsentGiven = row['DRCONSGIV'],
                        DriverSearchConducted = row['DRVSRCHCOND'],
                        DriverSearchConductedBy = row['DRVSRCHCONDBY'],
                        PassengerConsentSearchRequested = row['PASSCONSREQ'],
                        PassengerConsentGiven = row['PASSCONSGIV'],
                        PassengerSearchConducted = row['PASSSRCHCOND'],
                        PassengerSearchConductedBy = row['PASSSRCHCONDBY'],
                        DriverPassengerContrabandFound = row['PASSDRVCONTRA'],
                        DriverPassengerDrugsFound = row['PASSDRVDRUGS'],
                        DriverPassengerDrugParaphernaliaFound = row['PASSDRVPARA'],
                        DriverPassengerAlcoholFound = row['PASSDRVALC'],
                        DriverPassengerWeaponFound = row['PASSDRVWEAP'],
                        DriverPassengerStolenPropertyFound = row['PASSDRVSTOLPROP'],
                        DriverPassengerOtherContrabandFound = row['PASSDRVOTHER'],
                        DriverPassengerDrugAmount = row['PASSDRVDRAMT'],
                        PoliceDogPerformSniffOfVehicle = row['DOGPERFSNIFF'],
                        PoliceDogAlertIfSniffed = row['DOGALERT'],
                        PoliceDogVehicleSearched = row['DOGALERTSRCH'],
                        PoliceDogContrabandFound = row['DOGALERTSRCHCONTRA'],
                        PoliceDogDrugsFound = row['DOGDRUG'],
                        PoliceDogDrugParaphernaliaFound = row['DOGPARA'],
                        PoliceDogAlcoholFound = row['DOGALC'],
                        PoliceDogWeaponFound = row['DOGWEAP'],
                        PoliceDogStolenPropertyFound = row['DOGSTOLPROP'],
                        PoliceDogOtherContrabandFound = row['DOGOTHER'],
                        PoliceDogDrugAmount = row['DOGDRAMT']
                )
            stop_objs.append(stop_obj)
            print(counter)

        except Exception as e:
            print('counter:',counter)
            print('error:',e)
            #ipdb.set_trace()

        if LOADER_DEBUG:
            if counter > 10:
                break

    print('loading',counter,'stops')
    Stop.objects.bulk_create(stop_objs)


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0013_load_2022_statewide'),
    ]

    operations = [
            migrations.RunPython(load_files)
            ]
