# Generated by Django 4.1 on 2023-05-23 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=99, null=True)),
                ('code', models.TextField(max_length=5, null=True)),
                ('fips', models.CharField(max_length=7, null=True)),
            ],
            options={
                'db_table': 'agencies',
            },
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(null=True)),
                ('record_ref', models.CharField(max_length=19)),
                ('AgencyCode', models.TextField()),
                ('AgencyName', models.CharField(max_length=100, null=True)),
                ('DateOfStop', models.DateField(null=True)),
                ('TimeOfStop', models.TimeField(null=True)),
                ('DurationOfStop', models.CharField(max_length=99, null=True)),
                ('ZIP', models.CharField(max_length=100, null=True)),
                ('VehicleMake', models.TextField(null=True)),
                ('VehicleYear', models.CharField(max_length=99, null=True)),
                ('DriversYearofBirth', models.CharField(max_length=99, null=True)),
                ('DriverSex', models.CharField(max_length=99, null=True)),
                ('DriverRace', models.CharField(max_length=99, null=True)),
                ('ReasonForStop', models.CharField(max_length=99, null=True)),
                ('TypeOfMovingViolation', models.CharField(max_length=10, null=True)),
                ('ResultOfStop', models.CharField(max_length=99, null=True)),
                ('BeatLocationOfStop', models.TextField(null=True)),
                ('VehicleConsentSearchRequested', models.CharField(max_length=99, null=True)),
                ('VehicleConsentGiven', models.CharField(max_length=99, null=True)),
                ('VehicleSearchConducted', models.CharField(max_length=99, null=True)),
                ('VehicleSearchConductedBy', models.CharField(max_length=99, null=True)),
                ('VehicleContrabandFound', models.CharField(max_length=99, null=True)),
                ('VehicleDrugsFound', models.CharField(max_length=99, null=True)),
                ('VehicleDrugParaphernaliaFound', models.CharField(max_length=99, null=True)),
                ('VehicleAlcoholFound', models.CharField(max_length=99, null=True)),
                ('VehicleWeaponFound', models.CharField(max_length=99, null=True)),
                ('VehicleStolenPropertyFound', models.CharField(max_length=99, null=True)),
                ('VehicleOtherContrabandFound', models.CharField(max_length=99, null=True)),
                ('VehicleDrugAmount', models.CharField(max_length=99, null=True)),
                ('DriverConsentSearchRequested', models.CharField(max_length=99, null=True)),
                ('DriverConsentGiven', models.CharField(max_length=99, null=True)),
                ('DriverSearchConducted', models.CharField(max_length=99, null=True)),
                ('DriverSearchConductedBy', models.CharField(max_length=99, null=True)),
                ('PassengerConsentSearchRequested', models.CharField(max_length=99, null=True)),
                ('PassengerConsentGiven', models.CharField(max_length=99, null=True)),
                ('PassengerSearchConducted', models.CharField(max_length=99, null=True)),
                ('PassengerSearchConductedBy', models.CharField(max_length=99, null=True)),
                ('DriverPassengerContrabandFound', models.CharField(max_length=99, null=True)),
                ('DriverPassengerDrugsFound', models.CharField(max_length=99, null=True)),
                ('DriverPassengerDrugParaphernaliaFound', models.CharField(max_length=99, null=True)),
                ('DriverPassengerAlcoholFound', models.CharField(max_length=99, null=True)),
                ('DriverPassengerWeaponFound', models.CharField(max_length=99, null=True)),
                ('DriverPassengerStolenPropertyFound', models.CharField(max_length=99, null=True)),
                ('DriverPassengerOtherContrabandFound', models.CharField(max_length=99, null=True)),
                ('DriverPassengerDrugAmount', models.CharField(max_length=99, null=True)),
                ('PoliceDogPerformSniffOfVehicle', models.CharField(max_length=99, null=True)),
                ('PoliceDogAlertIfSniffed', models.CharField(max_length=99, null=True)),
                ('PoliceDogVehicleSearched', models.CharField(max_length=99, null=True)),
                ('PoliceDogContrabandFound', models.CharField(max_length=99, null=True)),
                ('PoliceDogDrugsFound', models.CharField(max_length=99, null=True)),
                ('PoliceDogDrugParaphernaliaFound', models.CharField(max_length=99, null=True)),
                ('PoliceDogAlcoholFound', models.CharField(max_length=99, null=True)),
                ('PoliceDogWeaponFound', models.CharField(max_length=99, null=True)),
                ('PoliceDogStolenPropertyFound', models.CharField(max_length=99, null=True)),
                ('PoliceDogOtherContrabandFound', models.CharField(max_length=99, null=True)),
                ('PoliceDogDrugAmount', models.CharField(max_length=99, null=True)),
                ('SearchConducted', models.CharField(max_length=99, null=True)),
                ('VehicleSearchType', models.CharField(max_length=99, null=True)),
                ('PassengersSearchType', models.CharField(max_length=99, null=True)),
                ('DriverSearchType', models.CharField(max_length=99, null=True)),
                ('ContrabandFound', models.CharField(max_length=99, null=True)),
                ('DrugsFound', models.CharField(max_length=99, null=True)),
                ('AlcoholFound', models.CharField(max_length=99, null=True)),
                ('ParaphernaliaFound', models.CharField(max_length=99, null=True)),
                ('WeaponFound', models.CharField(max_length=99, null=True)),
                ('StolenPropertyFound', models.CharField(max_length=99, null=True)),
                ('OtherContrabandFound', models.CharField(max_length=99, null=True)),
                ('DrugQuantity', models.CharField(max_length=99, null=True)),
                ('ConsentSearchRequested', models.CharField(max_length=99, null=True)),
                ('WasConsentGranted', models.CharField(max_length=99, null=True)),
                ('WasConsentSearchPerformed', models.CharField(max_length=99, null=True)),
                ('WasConsentContrabandFound', models.CharField(max_length=99, null=True)),
                ('ConsentDrugsFound', models.CharField(max_length=99, null=True)),
                ('ConsentAlcoholFound', models.CharField(max_length=99, null=True)),
                ('ConsentParaphernaliaFound', models.CharField(max_length=99, null=True)),
                ('ConsentWeaponFound', models.CharField(max_length=99, null=True)),
                ('ConsentStolenPropertyFound', models.CharField(max_length=99, null=True)),
                ('ConsentOtherContrabandFound', models.CharField(max_length=99, null=True)),
                ('ConsentDrugQuantity', models.CharField(max_length=99, null=True)),
                ('TypeOfRoadway', models.CharField(max_length=99, null=True)),
                ('Passenger1SearchType', models.CharField(max_length=99, null=True)),
                ('Passenger2SearchType', models.CharField(max_length=99, null=True)),
                ('Passenger3SearchType', models.CharField(max_length=99, null=True)),
                ('Passenger4SearchType', models.CharField(max_length=99, null=True)),
                ('Passenger5SearchType', models.CharField(max_length=99, null=True)),
                ('Passenger6SearchType', models.CharField(max_length=99, null=True)),
                ('driver_race', models.CharField(max_length=20, null=True)),
                ('search_conducted', models.BooleanField(null=True)),
                ('search_hit', models.BooleanField(null=True)),
                ('consent_search_requested', models.BooleanField(null=True)),
                ('consent_search_conducted', models.BooleanField(null=True)),
                ('dog_sniff', models.BooleanField(null=True)),
                ('dog_search_conducted', models.BooleanField(null=True)),
                ('dog_search_hit', models.BooleanField(null=True)),
                ('outcome', models.CharField(max_length=99, null=True)),
                ('Agency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='stops.agency')),
            ],
            options={
                'db_table': 'stops',
            },
        ),
    ]
