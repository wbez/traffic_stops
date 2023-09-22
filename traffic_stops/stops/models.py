from django.db import models
from collections import OrderedDict

# for checking if searches match list of true values
trues = ['1','1.00','Yes','True']
# TODO: standardize values
# for B01001 sex by race by age pops
table_codes = { 
        'white_nh': 'H', # White Alone, Not Hispanic or Latino
        'hispanic': 'I', # Hispanic or Latino
        'black':    'B', # Black or African American Alone
        'ai_an':    'C', # American Indian and Alaska Native Alone
        'asian':    'D', # Asian Alone
        'h_opi':    'E', # Native Hawaiian and Other Pacific Islander Alone
        }



class Agency(models.Model):
    class Meta:
        db_table = 'agencies'

    name = models.CharField(max_length=99,null=True)
    code = models.TextField(max_length=5,null=True)
    # all census data is 18+ TODO relabel these fields accordingly
    geoid = models.CharField(max_length=7,null=True)
    total_pop = models.IntegerField(null=True)
    latino = models.IntegerField(null=True)
    white_nh = models.IntegerField(null=True)
    black_nh = models.IntegerField(null=True)
    aian_nh = models.IntegerField(null=True)
    nhpi_nh = models.IntegerField(null=True)
    asian_nh = models.IntegerField(null=True)
    other = models.IntegerField(null=True)
    two_or_more = models.IntegerField(null=True)

    def adult_pop_by_race(self,totals=False,pct=True):
        """
        sum up and return the totals and pcts 
        of rough driving population (18+) 
        for each racial group 
        work in progress but it's config'd to return 
        either pcts or totals, could be both
        """
        # keep track
        total_data = OrderedDict({
                'total_pop': self.total_pop,
                'white_nh': self.white_nh,
                'hispanic': self.latino,
                'black': self.black_nh,
                'ai_an': self.aian_nh,
                'asian': self.asian_nh,
                'h_opi': self.nhpi_nh,
                'other': self.other,
                'two_or_more': self.two_or_more,
                })
        if pct:
            pct_data = {}
            # get list of dict keys to iterate through
            keys = [x for x in total_data.keys()]
            # calc pct by race
            for key in keys:
                # skip total field, and any nulls
                if key != 'total_pop' and total_data[key]:
                    # divide race by total
                    pct_data[key] = round(total_data[key]/total_data['total_pop']*100,1)
        
        # inelegant
        if pct:
            return pct_data
        
        if totals:
            return total_data

        
    def pct_blk_drivers_stopped(self,year=2022):
        """
        what pct of drivers stopped are black last year?
        """
        last_year_stops = self.stop_set.filter(year=year)
        black_drivers_last_year = last_year_stops.filter(driver_race='Black')
        if last_year_stops:
            return len(black_drivers_last_year)/len(last_year_stops)


    def ratio_blk_drivers_stopped_to_driving_pop(self):
        """
        the ratio of black drivers stop share 
        compared to black driving population share.
        large numbers are red flags
        """
        # get adult driving pop by race w/ pcts
        driving_pop = self.adult_pop_by_race(pct=True)
        # make sure we have data
        if driving_pop and driving_pop['total_pop'] and 'black_nh_pct' in driving_pop:
            blk_driving_pct = driving_pop['black_nh_pct']
            blk_stop_pct = self.pct_blk_drivers_stopped()
            if blk_stop_pct and blk_driving_pct:
                return blk_stop_pct/blk_driving_pct


class AgencyData(models.Model):
    """
    this table allows us to store
    agency-level data points
    without schema migrations
    """
    class Meta:
        db_table = 'agency_data'
    agency = models.ForeignKey(Agency,on_delete=models.CASCADE)
    agency_name = models.CharField(max_length=99)
    year = models.CharField(max_length=20,null=True)
    metric = models.CharField(max_length=99)
    value = models.CharField(max_length=99,null=True)
    rank = models.IntegerField(null=True)
    notes = models.CharField(max_length=99)


# Create your models here.
class Stop(models.Model):
    # metadata
    class Meta:
        db_table = 'stops'
    year = models.IntegerField(null=True) 
    record_ref = models.CharField(max_length=19)

    # 2012+ schema
    AgencyCode = models.TextField()
    AgencyName = models.CharField(max_length=100,null=True)
    agency = models.ForeignKey(Agency,null=True,on_delete=models.SET_NULL)
    DateOfStop = models.DateField(null=True)
    TimeOfStop = models.TimeField(null=True)
    # TODO: int/float
    DurationOfStop = models.CharField(max_length=99,null=True) # minutes?
    ZIP = models.CharField(max_length=100,null=True)
    VehicleMake = models.TextField(null=True)
    VehicleYear = models.CharField(max_length=99,null=True)
    # TODO: int/float
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
    # TODO: float
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
    # TODO: float
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
    # TODO: float
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
    # TODO: float
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
    # TODO: float
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
            # TODO return Latino
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
            or self.SearchConducted in trues \
            or self.get_consent_search_conducted()

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
            or self.PassengerConsentGiven in trues\
            or self.DriverSearchType == 'Consent'\
            or self.PassengerSearchType == 'Consent'\
            or self.VehicleSearchType == 'Consent'\
            or self.Passenger1SearchType == 'Consent'\
            or self.Passenger2SearchType == 'Consent'\
            or self.Passenger3SearchType == 'Consent'\
            or self.Passenger4SearchType == 'Consent'\
            or self.Passenger5SearchType == 'Consent'\
            or self.Passenger6SearchType == 'Consent'

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


