# Generated by Django 4.1 on 2022-09-01 21:55

from django.db import migrations
from stops.models import Stop
import csv
import ipdb
from traffic_stops.settings import BASE_DIR

### START CONFIG ###
data_dir = str(BASE_DIR) + '/data/'
path_to_data_file = data_dir + '2019_ITSS_Statewide_Redacted.txt'
### END CONFIG ###

stops = []
# TODO: figure out encoding for text files, translate to something workable
# e.g. fix line breaks, delimeters, encoding, etc.
# TODO: replace row indices with field names
# TODO: track agencies separately

def load_data(apps,schema_editor):
    data_file = open(path_to_data_file)
    data_csv = csv.DictReader(data_file,delimiter='~')

    for row in data_csv:
        try:
            stop_obj = Stop(
                        AgencyCode = row['AgencyCode'],
                        AgencyName = row['AgencyName'],
                        DateOfStop = row['DateOfStop'],
                        TimeOfStop = row['TimeOfStop'],
                        DurationOfStop = row['DurationOfStop'],
                        zipcode = row['ZIP'],
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
                        VehicleDrugParaphernaliaFound = row['VehicleDrugParahernaliaFound'],
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
                        PoliceDogDrugParaphernaliaFound = row['PoliceDogDrugParahernaliaFound'],
                        PoliceDogAlcoholFound = row['PoliceDogAlcoholFound'],
                        PoliceDogWeaponFound = row['PoliceDogWeaponFound'],
                        PoliceDogStolenPropertyFound = row['PoliceDogStolenPropertyFound'],
                        PoliceDogOtherContrabandFound = row['PoliceDogOtherContrabandFound'],
                        PoliceDogDrugAmount = row['PoliceDogDrugAmount']
                )
            stops.append(stop_obj)

        except Exception as e:
            print(e)
            #ipdb.set_trace()

    
    Stop.objects.bulk_create(stops)
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0001_initial'),
    ]

    operations = [
            migrations.RunPython(load_data)
    ]
