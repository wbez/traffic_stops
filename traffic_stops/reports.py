import csv
from django.db import connection
from stops.models import Stop
from traffic_stops.settings import BASE_DIR

### START CONFIGS ###
# output
outfile_dir = str(BASE_DIR) + '/reports/'
stop_headers = list(Stop.objects.first().__dict__.keys())[1:]
# metadata
agency_codes = [x[0] for x in connection.cursor().execute("select distinct AgencyCode from stops_stop")]
# update years - ranges don't include last number
years = [x for x in range(2004,2022)]
# db stuff
cursor = connection.cursor()
race_categories = ['White','Hispanic','Black','Native Hawaiian/Pacific Islander','Asian','Native American']
### END CONFIGS ###


def agency_report():
    """
    for each agency,
    export all their stop data
    to a csv
    """
    for agency_code in agency_codes:
        try:
            data = Stop.objects.raw('select * from stops_stop where AgencyCode = "' + agency_code + '"')
            agency_name = Stop.objects.filter(AgencyCode=agency)[0].AgencyName
            outfile = open(outfile_dir + agency_name + '.csv','w')
            outcsv = csv.DictWriter(outfile,stop_headers)
            outcsv.writeheader()
            for row in data.iterator():
                # remove extraneous metadata field
                row.__dict__.pop('_state')
                # write row as dict
                outcsv.writerow(row.__dict__)
            outfile.close()
            print(agency_name)
        except Exception as e:
            print(agency_name,'!@#$%^&*( ERROR !@#$%^&*()')
            import ipdb; ipdb.set_trace()


def stops_searches_citations_by_race(agency_code=None,year=None):
    """
    total stops, searches, citations
    by race
    """
    # queries
    stops_q = "select count(*) from stops_stop where driver_race = %s"
    if agency_code:
        stops_q += " and AgencyCode=" + agency_code
    if year:
        stops_q += 'and year =' + str(year)
    searches_q = stops_q + " and search_conducted = 1"
    citations_q = stops_q + " and outcome = 'Citation'"
    # data to return
    data = {
            'stops':{},
            'searches':{},
            'citations':{}
            }
    # stops
    for race in race_categories:
        data['stops'][race] = cursor.execute(stops_q,[race]).fetchone()[0]
    # searches
    for race in race_categories:
        data['searches'][race] = cursor.execute(searches_q,[race]).fetchone()[0]
    # citations
    for race in race_categories:
        data['citations'][race] = cursor.execute(citations_q,[race]).fetchone()[0]
    # totals and pcts by category
    for cat in data:
        data[cat]['total'] = sum([data[cat][race] for race in race_categories])
    # return
    return data


def ssc_over_time(agency_code=None,writeout=True):
    """
    a wrapper for stops_searches_citations_by_race
    that iterates over every year 
    and outputs csv
    """
    # collect data from stops_searches_citations_by_race()
    year_data = []
    for year in years:
        print(year)
        data = stops_searches_citations_by_race(agency_code=agency_code,year=year)
        data['year'] = year
        year_data.append(data)
    
    # writeout
    if writeout:
        try:
            headers = ['year']
            # get stop categories from data keys, except year
            stop_categories = [x for x in year_data[0] if x!= 'year']
            # splice together header categories, minus year, plus totals
            for race in race_categories + ['total']:
                for stop_category in stop_categories:
                    headers.append(race + '_driver_' + stop_category)
            # only adds agency name if an agency code was specified
            agency_name = ''
            if agency_code:
                agency_name = '-' + Stops.objects.filter(AgencyCode=agency_code).first().AgencyName
            # setup output file
            outfile_path = outfile_dir + 'ssc_over_time' + agency_name + '.csv'
            outfile = open(outfile_path,'w')
            outcsv = csv.DictWriter(outfile,headers)
            outcsv.writeheader()

            # write data
            for year in year_data:
                row_data = {'year':year['year']}
                # restructure rows
                for category in stop_categories:
                    for race in year[category]:
                        row_data[race + '_driver_' + category] = year[category][race]
                outcsv.writerow(row_data)
            # close file
            outfile.close()
        except Exception as e:
            print(e)
            import ipdb; ipdb.set_trace()
    # return
    return year_data
