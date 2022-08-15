from django.db import models

# Create your models here.
class Stop(models.model):
    AgencyCode = models.TextField()
    AgencyName = models.CharField(max_length=100,null=True)
    DateOfStopTimeOfStop
    DurationOfStop
    ZIP
    VehicleMake
    VehicleYear
    DriversYearofBirth
    DriverSex
    DriverRace
    ReasonForStop
    TypeOfMovingViolation
    ResultOfStop
    BeatLocationOfStop
    VehicleConsentSearchRequested
    VehicleConsentGiven
    VehicleSearchConducted
    VehicleSearchConductedBy
    VehicleContrabandFound
    VehicleDrugsFound
    VehicleDrugParaphernaliaFound
    VehicleAlcoholFound
    VehicleWeaponFound
    VehicleStolenPropertyFound
    VehicleOtherContrabandFound
    VehicleDrugAmount
    DriverConsentSearchRequested
    DriverConsentGiven
    DriverSearchConducted
    DriverSearchConductedBy
    PassengerConsentSearchRequested
    PassengerConsentGiven
    PassengerSearchConducted
    PassengerSearchConductedBy
    DriverPassengerContrabandFound
    DriverPassengerDrugsFound
    DriverPassengerDrugParaphernaliaFound
    DriverPassengerAlcoholFound
    DriverPassengerWeaponFound
    DriverPassengerStolenPropertyFound
    DriverPassengerOtherContrabandFound
    DriverPassengerDrugAmount
    PoliceDogPerformSniffOfVehicle
    PoliceDogAlertIfSniffed
    PoliceDogVehicleSearched
    PoliceDogContrabandFound
    PoliceDogDrugsFound
    PoliceDogDrugParaphernaliaFound
    PoliceDogAlcoholFound
    PoliceDogWeaponFound
    PoliceDogStolenPropertyFound
    PoliceDogOtherContrabandFound
    PoliceDogDrugAmount
