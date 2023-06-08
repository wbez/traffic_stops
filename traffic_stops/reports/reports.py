import csv
from django.db import connection
from stops.models import Stop, Agency
from traffic_stops.settings import BASE_DIR
from reports.utils import get_rate

### START CONFIGS ###
# output
outfile_dir = str(BASE_DIR) + '/reports/output/'
stop_headers = list(Stop.objects.first().__dict__.keys())[1:]
# metadata
agency_codes = [x['code'] for x in Agency.objects.values('code').distinct()]
# update years - ranges don't include last number
years = [x for x in range(2004022)]
# db stuff
cursor = connection.cursor()
#race_categories = ['White','Hispanic','Black','Native Hawaiian/Pacific Islander','Asian','Native American']
race_categories = [x['driver_race'] for x in Stop.objects.values('driver_race').distinct()]
### END CONFIGS ###

def write_out(name,data):
    """
    create file {name}
    using {data} for rows 
    and {data} keys for headers
    """
    output_folder = outfile_dir
    output_path = outfile_dir + name + '.csv'
    headers = data[0].keys()
    output_file = open(output_path,'w')
    output_csv = csv.DictWriter(output_file,headers)
    output_csv.writeheader()
    output_csv.writerows(data)
    output_file.close()
    print('writing out to', output_path)


def agencies_report(year=None):
    """
    each agency's stops, searches, citations
    by race
    together in one csv
    """
    # will write this to spreadsheet
    data = []
    # loop through
    for agency in Agency.objects.all():
        # main query is all agency stops
        stops = agency.stop_set.all()
 
        # filter by year if provided
        if year:
            stops = stops.filter(year=year)
       
        # stops
        black_driver_stops = stops.filter(driver_race='Black')
        white_driver_stops = stops.filter(driver_race='White')
        latino_driver_stops = stops.filter(driver_race='Hispanic')
        
        # searches
        black_driver_searches = black_driver_stops.filter(search_conducted=True)
        white_driver_searches = white_driver_stops.filter(search_conducted=True)
        latino_driver_searches = latino_driver_stops.filter(search_conducted=True) 
       
        # consent searches
        black_driver_consent_searches = black_driver_stops.filter(consent_search_conducted=True)
        white_driver_consent_searches = white_driver_stops.filter(consent_search_conducted=True)
        latino_driver_consent_searches = latino_driver_stops.filter(consent_search_conducted=True) 

        # dog searches
        black_driver_dog_searches = black_driver_stops.filter(dog_search_conducted=True)
        white_driver_dog_searches = white_driver_stops.filter(dog_search_conducted=True)
        latino_driver_dog_searches = latino_driver_stops.filter(dog_search_conducted=True) 
        
        # search hits
        black_driver_search_hits = black_driver_stops.filter(search_hit=True)
        white_driver_search_hits = white_driver_stops.filter(search_hit=True)
        latino_driver_search_hits = latino_driver_stops.filter(search_hit=True)

        # tickets
        black_driver_tickets = black_driver_stops.filter(outcome='Citation')
        white_driver_tickets = white_driver_stops.filter(outcome='Citation')
        latino_driver_tickets = latino_driver_stops.filter(outcome='Citation')
        
        # add stuff to csv row
        row = {
                'Agency':agency.name,
                'Total stops': stops.count(),
                'Black driver stops': black_driver_stops.count(),
                'White driver stops': white_driver_stops.count(),
                'Latino driver stops': latino_driver_stops.count(),
                'Black driver searches': black_driver_searches.count(),
                'White driver searches': white_driver_searches.count(),
                'Latino driver searches': latino_driver_searches.count(),
                'Black driver search rate': get_rate(black_driver_searches.count(),black_driver_stops.count()),
                'White driver search rate': get_rate(white_driver_searches.count(),white_driver_stops.count()),
                'Latino driver search rate': get_rate(latino_driver_searches.count(),latino_driver_stops.count()),
                'Black driver consent search rate': get_rate(black_driver_consent_searches.count(),black_driver_stops.count()),
                'White driver consent search rate': get_rate(white_driver_consent_searches.count(),white_driver_stops.count()),
                'Latino driver consent search rate': get_rate(latino_driver_consent_searches.count(),latino_driver_stops.count()),
                'Black driver dog search rate': get_rate(black_driver_dog_searches.count(),black_driver_stops.count()),
                'White driver dog search rate': get_rate(white_driver_dog_searches.count(),white_driver_stops.count()),
                'Latino driver dog search rate': get_rate(latino_driver_dog_searches.count(),latino_driver_stops.count()),
                'Black driver search hit rate': get_rate(black_driver_search_hits.count(),black_driver_stops.count()),
                'White driver search hit rate': get_rate(white_driver_search_hits.count(),white_driver_stops.count()),
                'Latino driver search hit rate': get_rate(latino_driver_search_hits.count(),latino_driver_stops.count()),
                'Black driver ticket rate': get_rate(black_driver_tickets.count(),black_driver_stops.count()),
                'White driver ticket rate': get_rate(white_driver_tickets.count(),white_driver_stops.count()),
                'Latino driver ticket rate': get_rate(latino_driver_tickets.count(),latino_driver_stops.count())
                }
        # add more stuff
        row['Black and white search rates?'] = 1 if row['Black driver search rate'] and row['White driver search rate'] else 0
        row['Black drivers searched more than white?'] = 1 if row['Black and white search rates?'] and row['Black driver search rate'] > row['White driver search rate'] else 0


        row['Black and white hit rates?'] = 1 if row['Black driver search hit rate'] and row['White driver search hit rate'] else 0
        row['Black driver hit rate lower than white?'] = 1 if row['Black and white hit rates?'] and row['Black driver search hit rate'] < row['White driver search hit rate'] else 0
        
        data.append(row)
        print(row['Agency'])

    # write out
    timeframe = str(year) if year else 'all_years'
    write_out('agency_report_' + timeframe,data)





def agency_export():
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
            print(agency_name,'ERROR')
            import ipdb; ipdb.set_trace()


def stops_searches_citations_by_race(agency_codes=None,year=None):
    """
    total stops, searches, citations
    by race
    """
    codes_string = ','.join([str(x) for x in agency_codes])
    # queries
    stops_q = "select count(*) from stops_stop where driver_race = %s"
    if agency_code:
        stops_q += " and AgencyCode in (" + codes_string +")"
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
