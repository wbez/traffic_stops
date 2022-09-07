from django.db import models

# Create your models here.
class Stop(models.Model):
    AgencyCode = models.TextField()
    AgencyName = models.CharField(max_length=100,null=True)
    DateOfStop = models.DateField()
    TimeOfStop = models.TimeField()
    DurationOfStop = models.IntegerField() # minutes?
    zipcode = models.IntegerField()
    VehicleMake = models.TextField()
    VehicleYear = models.IntegerField()
    DriversYearofBirth = models.IntegerField()
    DriverSex = models.IntegerField()
    DriverRace = models.IntegerField()
    ReasonForStop = models.IntegerField()
    TypeOfMovingViolation = models.IntegerField()
    ResultOfStop = models.IntegerField()
    BeatLocationOfStop = models.TextField()
    VehicleConsentSearchRequested  = models.IntegerField()
    VehicleConsentGiven  = models.IntegerField()
    VehicleSearchConducted  = models.IntegerField()
    VehicleSearchConductedBy  = models.IntegerField()
    VehicleContrabandFound  = models.IntegerField()
    VehicleDrugsFound  = models.IntegerField()
    VehicleDrugParaphernaliaFound  = models.IntegerField()
    VehicleAlcoholFound  = models.IntegerField()
    VehicleWeaponFound  = models.IntegerField()
    VehicleStolenPropertyFound  = models.IntegerField()
    VehicleOtherContrabandFound  = models.IntegerField()
    VehicleDrugAmount  = models.IntegerField()
    DriverConsentSearchRequested  = models.IntegerField()
    DriverConsentGiven  = models.IntegerField()
    DriverSearchConducted  = models.IntegerField()
    DriverSearchConductedBy  = models.IntegerField()
    PassengerConsentSearchRequested  = models.IntegerField()
    PassengerConsentGiven  = models.IntegerField()
    PassengerSearchConducted  = models.IntegerField()
    PassengerSearchConductedBy  = models.IntegerField()
    DriverPassengerContrabandFound  = models.IntegerField()
    DriverPassengerDrugsFound  = models.IntegerField()
    DriverPassengerDrugParaphernaliaFound  = models.IntegerField()
    DriverPassengerAlcoholFound  = models.IntegerField()
    DriverPassengerWeaponFound  = models.IntegerField()
    DriverPassengerStolenPropertyFound  = models.IntegerField()
    DriverPassengerOtherContrabandFound  = models.IntegerField()
    DriverPassengerDrugAmount  = models.IntegerField()
    PoliceDogPerformSniffOfVehicle  = models.IntegerField()
    PoliceDogAlertIfSniffed  = models.IntegerField()
    PoliceDogVehicleSearched  = models.IntegerField()
    PoliceDogContrabandFound  = models.IntegerField()
    PoliceDogDrugsFound  = models.BooleanField()
    PoliceDogDrugParaphernaliaFound  = models.IntegerField()
    PoliceDogAlcoholFound  = models.IntegerField()
    PoliceDogWeaponFound  = models.IntegerField()
    PoliceDogStolenPropertyFound  = models.IntegerField()
    PoliceDogOtherContrabandFound  = models.IntegerField()
    PoliceDogDrugAmount  = models.BooleanField()


class OldStop(models.Model):
    AgencyName = models.CharField(max_length=100,null=True))
    DateOfStop = models.DateField()
    TimeOfStop = models.TimeField()
    Location = models.TextField()
    BeatLocation = models.TextField()
    Gender = models.IntegerField()
    Race = models.IntegerField()
    ReasonForSearchDrug = models.IntegerField()
    ReasonForSearchFitsDescriptionRadio = models.IntegerField()
    ReasonForSearchFitsDescriptionWitness = models.IntegerField()
    ReasonForSearchCasing = models.IntegerField()
    ReasonForSearchProximity = models.IntegerField()
    ReasonForSearchGangEnforcement = models.IntegerField()
    ReasonForSearchSuspiciousActivity = models.IntegerField()
    ReasonForSearchOther = models.IntegerField()
    ReasonForSearchSpecifyOther = models.TextField()
    FriskWasConducted = models.IntegerField()
    FriskConductedBy = models.IntegerField()
    ReasonForFriskVerbalThreats = models.IntegerField()
    ReasonForFriskPriorKnowlege = models.IntegerField()
    ReasonForFriskViolentActions = models.IntegerField() #ReasonForFriskViolentAcitons
    ReasonForFriskViolentCrime = models.IntegerField()
    ReasonForFriskSuspisiousBulge = models.IntegerField()
    ReasonForFriskEvasive = models.IntegerField()
    ReasonForFriskOther = models.IntegerField()
    ReasonForFriskSpecifyOther = models.CharField(max_length=100,null=True)
    FriskLedToSearchBeyond = models.IntegerField()
    SearchBeyondWasConducted = models.IntegerField()
    SearchBeyondConductedBy = models.IntegerField()
    ReasonForSearchBeyondDrugParaphernalia = models.IntegerField()
    ReasonForSearchBeyondHardObject = models.IntegerField()
    ReasonForSearchBeyondFirearm = models.IntegerField()
    ReasonForSearchBeyondOtherWeapon = models.IntegerField()
    ReasonForSearchBeyondOther = models.IntegerField()
    ReasonForSearchBeyondSpecifyOther = models.CharField(max_length=100,null=True)
    SearchBeyondFoundContraband = models.IntegerField()
    SearchBeyondFoundDrugs = models.IntegerField()
    SearchBeyondFoundDrugParaphernalia = models.IntegerField()
    SearchBeyondFoundAlcohol = models.IntegerField()
    SearchBeyondFoundWeapon = models.IntegerField()
    SearchBeyondFoundStolenProperty = models.IntegerField()
    SearchBeyondFoundOther = models.IntegerField()
    SearchBeyondAmountOfDrugsFound = models.IntegerField()
    WarningCitationIssued = models.IntegerField()
    Arrest = models.IntegerField()
    ViolationsOrCharges = models.CharField(max_length=100,null=True)






# TODO: model for agencies
