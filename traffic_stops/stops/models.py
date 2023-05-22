from django.db import models

# for checking if searches match list of true values
trues = ['1','1.00','Yes','True']
# TODO: standardize values


# Create your models here.
class Stop(models.Model):
    # 2012+ schema
    AgencyCode = models.TextField()
    AgencyName = models.CharField(max_length=100,null=True)
    year = models.IntegerField(null=True) 
    DateOfStop = models.DateField(null=True)
    TimeOfStop = models.TimeField(null=True)
    DurationOfStop = models.CharField(max_length=99,null=True) # minutes?
    ZIP = models.CharField(max_length=100,null=True)
    VehicleMake = models.TextField(null=True)
    VehicleYear = models.CharField(max_length=99,null=True)
    DriversYearofBirth = models.CharField(max_length=99,null=True)
    DriverSex = models.CharField(max_length=99,null=True)
    DriverRace = models.CharField(max_length=99,null=True)
    ReasonForStop = models.CharField(max_length=99,null=True)
    TypeOfMovingViolation = models.CharField(max_length=10,null=True)
    ResultOfStop = models.CharField(max_length=99,null=True)
    BeatLocationOfStop = models.TextField(null=True)
    VehicleConsentSearchRequested  = models.CharField(max_length=99,null=True)
    VehicleConsentGiven  = models.CharField(max_length=99,null=True)
    VehicleSearchConducted  = models.CharField(max_length=99,null=True)
    VehicleSearchConductedBy  = models.CharField(max_length=99,null=True)
    VehicleContrabandFound  = models.CharField(max_length=99,null=True)
    VehicleDrugsFound  = models.CharField(max_length=99,null=True)
    VehicleDrugParaphernaliaFound  = models.CharField(max_length=99,null=True)
    VehicleAlcoholFound  = models.CharField(max_length=99,null=True)
    VehicleWeaponFound  = models.CharField(max_length=99,null=True)
    VehicleStolenPropertyFound  = models.CharField(max_length=99,null=True)
    VehicleOtherContrabandFound  = models.CharField(max_length=99,null=True)
    VehicleDrugAmount  = models.CharField(max_length=99,null=True)
    DriverConsentSearchRequested  = models.CharField(max_length=99,null=True)
    DriverConsentGiven  = models.CharField(max_length=99,null=True)
    DriverSearchConducted  = models.CharField(max_length=99,null=True)
    DriverSearchConductedBy  = models.CharField(max_length=99,null=True)
    PassengerConsentSearchRequested  = models.CharField(max_length=99,null=True)
    PassengerConsentGiven  = models.CharField(max_length=99,null=True)
    PassengerSearchConducted  = models.CharField(max_length=99,null=True)
    PassengerSearchConductedBy  = models.CharField(max_length=99,null=True)
    DriverPassengerContrabandFound  = models.CharField(max_length=99,null=True)
    DriverPassengerDrugsFound  = models.CharField(max_length=99,null=True)
    DriverPassengerDrugParaphernaliaFound  = models.CharField(max_length=99,null=True)
    DriverPassengerAlcoholFound  = models.CharField(max_length=99,null=True)
    DriverPassengerWeaponFound  = models.CharField(max_length=99,null=True)
    DriverPassengerStolenPropertyFound  = models.CharField(max_length=99,null=True)
    DriverPassengerOtherContrabandFound  = models.CharField(max_length=99,null=True)
    DriverPassengerDrugAmount  = models.CharField(max_length=99,null=True)
    PoliceDogPerformSniffOfVehicle  = models.CharField(max_length=99,null=True)
    PoliceDogAlertIfSniffed  = models.CharField(max_length=99,null=True)
    PoliceDogVehicleSearched  = models.CharField(max_length=99,null=True)
    PoliceDogContrabandFound  = models.CharField(max_length=99,null=True)
    PoliceDogDrugsFound  = models.CharField(max_length=99,null=True)
    PoliceDogDrugParaphernaliaFound  = models.CharField(max_length=99,null=True)
    PoliceDogAlcoholFound  = models.CharField(max_length=99,null=True)
    PoliceDogWeaponFound  = models.CharField(max_length=99,null=True)
    PoliceDogStolenPropertyFound  = models.CharField(max_length=99,null=True)
    PoliceDogOtherContrabandFound  = models.CharField(max_length=99,null=True)
    PoliceDogDrugAmount  = models.CharField(max_length=99,null=True)

    #2007-2011
    SearchConducted  = models.CharField(max_length=99,null=True)
    VehicleSearchType = models.CharField(max_length=99,null=True) # need to add a derived field to reconcile this with 2012+ data
    PassengersSearchType = models.CharField(max_length=99,null=True) # need to add derived field
    DriverSearchType = models.CharField(max_length=99,null=True) # need to add derived field
    ContrabandFound = models.CharField(max_length=99,null=True)
    DrugsFound = models.CharField(max_length=99,null=True)
    AlcoholFound = models.CharField(max_length=99,null=True)
    ParaphernaliaFound = models.CharField(max_length=99,null=True)
    WeaponFound = models.CharField(max_length=99,null=True)
    StolenPropertyFound = models.CharField(max_length=99,null=True)
    OtherContrabandFound = models.CharField(max_length=99,null=True)
    DrugQuantity = models.CharField(max_length=99,null=True) # need to derive this to reconcile with 2012 via max()
    ConsentSearchRequested = models.CharField(max_length=99,null=True)
    WasConsentGranted = models.CharField(max_length=99,null=True)
    WasConsentSearchPerformed = models.CharField(max_length=99,null=True)
    WasConsentContrabandFound = models.CharField(max_length=99,null=True)
    ConsentDrugsFound = models.CharField(max_length=99,null=True)
    ConsentAlcoholFound = models.CharField(max_length=99,null=True)
    ConsentParaphernaliaFound = models.CharField(max_length=99,null=True)
    ConsentWeaponFound = models.CharField(max_length=99,null=True)
    ConsentStolenPropertyFound = models.CharField(max_length=99,null=True)
    ConsentOtherContrabandFound = models.CharField(max_length=99,null=True)
    ConsentDrugQuantity = models.CharField(max_length=99,null=True)

    # 2004-2006
    TypeOfRoadway = models.CharField(max_length=99,null=True)
    Passenger1SearchType = models.CharField(max_length=99,null=True)
    Passenger2SearchType = models.CharField(max_length=99,null=True)
    Passenger3SearchType = models.CharField(max_length=99,null=True)
    Passenger4SearchType = models.CharField(max_length=99,null=True)
    Passenger5SearchType = models.CharField(max_length=99,null=True)
    Passenger6SearchType = models.CharField(max_length=99,null=True)

    # summary fields
    driver_race = models.CharField(max_length=20,null=True)
    search_conducted = models.BooleanField(null=True)
    search_hit = models.BooleanField(null=True)
    consent_search_requested = models.BooleanField(null=True)
    consent_search_conducted = models.BooleanField(null=True)
    dog_sniff = models.BooleanField(null=True)
    dog_search_conducted = models.BooleanField(null=True)
    dog_search_hit = models.BooleanField(null=True)
    outcome = models.CharField(max_length=99,null=True)

    # summary field methods
    def get_driver_race(self):
        if self.DriverRace in ('Caucasian','1','1.00'):
            return 'White'
        elif self.DriverRace in ('African American','2','2.00'):
            return 'Black'
        elif self.DriverRace in ('Native American/Alaskan','3','3.00'):
            return 'Native American'
        elif self.DriverRace in ('Hispanic','4','4.00'):
            return 'Hispanic'
        # note that Asian / PI split up in later years, so now it's difficult to compare across time
        elif self.DriverRace in ('Asian/Pacific Islander','5','5.00'):
            return 'Asian'
        elif self.DriverRace in ('6','6.00'):
            return 'Native Hawaiian/Pacific Islander'

    def get_search_conducted(self):
        return self.VehicleSearchConducted in trues \
            or self.DriverSearchConducted in trues \
            or self.PassengerSearchConducted in trues \
            or self.SearchConducted in trues

    def get_search_hit(self):
        # only count the hit if there was a search?
        return self.get_search_conducted()\
            and (\
                # note there could be weird mix of vehicle/pass searches/hits
                self.VehicleContrabandFound in trues\
                or self.VehicleDrugsFound in trues\
                or self.VehicleDrugParaphernaliaFound in trues\
                or self.VehicleAlcoholFound in trues\
                or self.VehicleWeaponFound in trues\
                or self.VehicleStolenPropertyFound in trues\
                or self.VehicleOtherContrabandFound in trues\
                or self.DriverPassengerDrugsFound in trues\
                or self.DriverPassengerDrugParaphernaliaFound in trues\
                or self.DriverPassengerAlcoholFound in trues\
                or self.DriverPassengerWeaponFound in trues\
                or self.DriverPassengerStolenPropertyFound in trues\
                or self.DriverPassengerOtherContrabandFound in trues\
                or self.DrugsFound in trues\
                or self.AlcoholFound in trues\
                or self.WeaponFound in trues\
                or self.ParaphernaliaFound in trues\
                or self.StolenPropertyFound in trues\
                or self.OtherContrabandFound in trues\
                # consent search hits
                or self.get_consent_search_hit()
                # dog search hits
                or self.get_dog_search_hit()
                )

    def get_consent_search_requested(self):
        return self.VehicleConsentSearchRequested in trues\
            or self.DriverConsentSearchRequested in trues\
            or self.PassengerConsentSearchRequested in trues\
            or self.ConsentSearchRequested in trues


    def get_consent_search_conducted(self):
        return self.WasConsentSearchPerformed in trues\
            or self.VehicleConsentGiven in trues\
            or self.DriverConsentGiven in trues\
            or self.PassengerConsentGiven in trues

    def get_consent_search_hit(self):
        return self.WasConsentContrabandFound in trues\
                or self.ConsentDrugsFound in trues\
                or self.ConsentAlcoholFound in trues\
                or self.ConsentParaphernaliaFound in trues\
                or self.ConsentWeaponFound in trues\
                or self.ConsentStolenPropertyFound in trues\
                or self.ConsentOtherContrabandFound in trues

    def get_dog_sniff(self):
        return self.PoliceDogPerformSniffOfVehicle in trues

    def get_dog_search_conducted(self):
        return self.PoliceDogVehicleSearched in trues

    def get_dog_search_hit(self):
        return self.PoliceDogContrabandFound in trues\
            or self.PoliceDogDrugsFound in trues\
            or self.PoliceDogDrugParaphernaliaFound in trues\
            or self.PoliceDogAlcoholFound in trues\
            or self.PoliceDogWeaponFound in trues\
            or self.PoliceDogStolenPropertyFound in trues\
            or self.PoliceDogOtherContrabandFound in trues

    def get_outcome(self):
        if self.ResultOfStop in ('1','1.00','Citation'):
            return 'Citation'
        elif self.ResultOfStop in ('2','2.00','Written Warning'):
            return 'Written Warning'
        elif self.ResultOfStop in ('3','3.00','Verbal Warning'):
            return 'Verbal Warning'




'''
is this the pedestrian stop schema?

class OldStop(models.Model):
    AgencyName = models.CharField(max_length=100,null=True)
    DateOfStop = models.DateField()
    TimeOfStop = models.TimeField()
    Location = models.TextField()
    BeatLocation = models.TextField()
    Gender = models.CharField(max_length=99,)
    Race = models.CharField(max_length=99,)
    ReasonForSearchDrug = models.CharField(max_length=99,)
    ReasonForSearchFitsDescriptionRadio = models.CharField(max_length=99,)
    ReasonForSearchFitsDescriptionWitness = models.CharField(max_length=99,)
    ReasonForSearchCasing = models.CharField(max_length=99,)
    ReasonForSearchProximity = models.CharField(max_length=99,)
    ReasonForSearchGangEnforcement = models.CharField(max_length=99,)
    ReasonForSearchSuspiciousActivity = models.CharField(max_length=99,)
    ReasonForSearchOther = models.CharField(max_length=99,)
    ReasonForSearchSpecifyOther = models.TextField()
    FriskWasConducted = models.CharField(max_length=99,)
    FriskConductedBy = models.CharField(max_length=99,)
    ReasonForFriskVerbalThreats = models.CharField(max_length=99,)
    ReasonForFriskPriorKnowlege = models.CharField(max_length=99,)
    ReasonForFriskViolentActions = models.CharField(max_length=99,) #ReasonForFriskViolentAcitons
    ReasonForFriskViolentCrime = models.CharField(max_length=99,)
    ReasonForFriskSuspisiousBulge = models.CharField(max_length=99,)
    ReasonForFriskEvasive = models.CharField(max_length=99,)
    ReasonForFriskOther = models.CharField(max_length=99,)
    ReasonForFriskSpecifyOther = models.CharField(max_length=100,null=True)
    FriskLedToSearchBeyond = models.CharField(max_length=99,)
    SearchBeyondWasConducted = models.CharField(max_length=99,)
    SearchBeyondConductedBy = models.CharField(max_length=99,)
    ReasonForSearchBeyondDrugParaphernalia = models.CharField(max_length=99,)
    ReasonForSearchBeyondHardObject = models.CharField(max_length=99,)
    ReasonForSearchBeyondFirearm = models.CharField(max_length=99,)
    ReasonForSearchBeyondOtherWeapon = models.CharField(max_length=99,)
    ReasonForSearchBeyondOther = models.CharField(max_length=99,)
    ReasonForSearchBeyondSpecifyOther = models.CharField(max_length=100,null=True)
    SearchBeyondFoundContraband = models.CharField(max_length=99,)
    SearchBeyondFoundDrugs = models.CharField(max_length=99,)
    SearchBeyondFoundDrugParaphernalia = models.CharField(max_length=99,)
    SearchBeyondFoundAlcohol = models.CharField(max_length=99,)
    SearchBeyondFoundWeapon = models.CharField(max_length=99,)
    SearchBeyondFoundStolenProperty = models.CharField(max_length=99,)
    SearchBeyondFoundOther = models.CharField(max_length=99,)
    SearchBeyondAmountOfDrugsFound = models.CharField(max_length=99,)
    WarningCitationIssued = models.CharField(max_length=99,)
    Arrest = models.CharField(max_length=99,)
    ViolationsOrCharges = models.CharField(max_length=100,null=True)


'''



# TODO: model for agencies
