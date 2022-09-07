# Generated by Django 4.1 on 2022-09-07 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AgencyCode', models.TextField()),
                ('AgencyName', models.CharField(max_length=100, null=True)),
                ('DateOfStop', models.DateField()),
                ('TimeOfStop', models.TimeField()),
                ('DurationOfStop', models.IntegerField()),
                ('zipcode', models.CharField(max_length=100, null=True)),
                ('VehicleMake', models.TextField()),
                ('VehicleYear', models.IntegerField()),
                ('DriversYearofBirth', models.IntegerField()),
                ('DriverSex', models.IntegerField()),
                ('DriverRace', models.IntegerField()),
                ('ReasonForStop', models.IntegerField()),
                ('TypeOfMovingViolation', models.IntegerField()),
                ('ResultOfStop', models.IntegerField()),
                ('BeatLocationOfStop', models.TextField()),
                ('VehicleConsentSearchRequested', models.IntegerField()),
                ('VehicleConsentGiven', models.IntegerField()),
                ('VehicleSearchConducted', models.IntegerField()),
                ('VehicleSearchConductedBy', models.IntegerField()),
                ('VehicleContrabandFound', models.IntegerField()),
                ('VehicleDrugsFound', models.IntegerField()),
                ('VehicleDrugParaphernaliaFound', models.IntegerField()),
                ('VehicleAlcoholFound', models.IntegerField()),
                ('VehicleWeaponFound', models.IntegerField()),
                ('VehicleStolenPropertyFound', models.IntegerField()),
                ('VehicleOtherContrabandFound', models.IntegerField()),
                ('VehicleDrugAmount', models.IntegerField()),
                ('DriverConsentSearchRequested', models.IntegerField()),
                ('DriverConsentGiven', models.IntegerField()),
                ('DriverSearchConducted', models.IntegerField()),
                ('DriverSearchConductedBy', models.IntegerField()),
                ('PassengerConsentSearchRequested', models.IntegerField()),
                ('PassengerConsentGiven', models.IntegerField()),
                ('PassengerSearchConducted', models.IntegerField()),
                ('PassengerSearchConductedBy', models.IntegerField()),
                ('DriverPassengerContrabandFound', models.IntegerField()),
                ('DriverPassengerDrugsFound', models.IntegerField()),
                ('DriverPassengerDrugParaphernaliaFound', models.IntegerField()),
                ('DriverPassengerAlcoholFound', models.IntegerField()),
                ('DriverPassengerWeaponFound', models.IntegerField()),
                ('DriverPassengerStolenPropertyFound', models.IntegerField()),
                ('DriverPassengerOtherContrabandFound', models.IntegerField()),
                ('DriverPassengerDrugAmount', models.IntegerField()),
                ('PoliceDogPerformSniffOfVehicle', models.IntegerField()),
                ('PoliceDogAlertIfSniffed', models.IntegerField()),
                ('PoliceDogVehicleSearched', models.IntegerField()),
                ('PoliceDogContrabandFound', models.IntegerField()),
                ('PoliceDogDrugsFound', models.IntegerField()),
                ('PoliceDogDrugParaphernaliaFound', models.IntegerField()),
                ('PoliceDogAlcoholFound', models.IntegerField()),
                ('PoliceDogWeaponFound', models.IntegerField()),
                ('PoliceDogStolenPropertyFound', models.IntegerField()),
                ('PoliceDogOtherContrabandFound', models.IntegerField()),
                ('PoliceDogDrugAmount', models.IntegerField()),
            ],
        ),
    ]
