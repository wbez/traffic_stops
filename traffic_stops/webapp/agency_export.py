import json, statistics
from collections import OrderedDict
from stops.models import Stop, Agency

### START CONFIG ###
outfile_path = 'webapp/output/agencies.json'
years = range(2004,2023)
# hard-coding because the state isn't really an agency but 
# but come to think of it could put this in ISP next time and share it w/ statewide
illinois_demo_pcts = OrderedDict({
    'latino':16.2,
    'white_nh':61.2,
    'black_nh':13.6,
    'aian_nh':0.1,
    'nhpi_nh':0,
    'asian_nh':6,
    'other':0.3,
    'two_or_more':2.6,
    })
illinois_copy_block = ''
debug = True # basically skips statewide query when True to speed up processing
debug_agencies = ['CHICAGO POLICE']
### END CONFIG ###
    

def shorten_year(year):
    return "'" + str(year)[-2:]


def missing_years_text(name,years):
    base = 'IDOT has no traffic stops on file for ' + name + ' in '
    if len(years) == 1:
        return base + str(years[0]) + '.'
    elif len(years) == 2:
        return base + str(years[0]) + ' or ' + str(years[1]) + '.'
    elif len(years) > 2:
        return base + ', '.join([str(x) for x in years[:-1]]) + ' or ' + str(years[-1]) + '.'


def get_statewide():
    # collect data
    data = []

    # statewide first
    row = {'name': 'Illinois statewide','chart_time_series':[]}

    # every year
    for year in years:
        print('statewide',year)
        # filter by year
        statewide_year = Stop.objects.filter(year=year)

        # save 2022 data for big numbers
        if year == 2022:
            statewide_22 = statewide_year

        # filter by race
        statewide_year_blk_drv_stops = statewide_year.filter(driver_race='Black')
        statewide_year_wh_drv_stops = statewide_year.filter(driver_race='White')
        statewide_year_latino_drv_stops = statewide_year.filter(driver_race='Hispanic')
        statewide_year_asian_drv_stops = statewide_year.filter(driver_race='Asian')
        statewide_year_na_drv_stops = statewide_year.filter(driver_race='Native American')
        statewide_year_nhpi_drv_stops = statewide_year.filter(driver_race='Native Hawaiian/Pacific Islander')
        row['chart_time_series'].append(
                OrderedDict({'year': shorten_year(year),
                'latino_drv_stops':len(statewide_year_latino_drv_stops),
                'wh_drv_stops':len(statewide_year_wh_drv_stops),
                'blk_drv_stops':len(statewide_year_blk_drv_stops),
                'na_drv_stops':len(statewide_year_na_drv_stops),
                'nhpi_drv_stops':len(statewide_year_nhpi_drv_stops),
                'asian_drv_stops':len(statewide_year_asian_drv_stops),
                'total_stops': len(statewide_year),
                })
            )
    
    # 2022 data
    print('statewide 2022')
    row['big_numbers'] = {}
    row['big_numbers']['stops'] = len(statewide_22)
    row['big_numbers']['searches'] = len(statewide_22.filter(search_conducted=True))
    row['big_numbers']['citations'] = len(statewide_22.filter(outcome='Citation'))
    row['demographics'] = illinois_demo_pcts
    # the whole state doesn't miss a year
    row['missing_years'] = None
    row['copy_block'] = build_copy(row)
    data.append(row)

    return data


def get_agencies():
    
    # collect data
    data = []

    # debug mode speeds up processing
    agencies = Agency.objects.all() if not debug else Agency.objects.filter(name__in=debug_agencies)

    # loop thru each agency
    for agency in agencies:
        counter = 0
        # keep track
        missing_years = []

        # title case, more or less
        agency_name = agency.get_name_cased()
        
        # set up row
        row = {'name':agency_name,'chart_time_series':[]}
        # loop through each year
        for year in years:
            # filter by year
            agency_year = agency.stop_set.filter(year=year)
            agency_year_list = list(agency_year)
            # keep track of missing years
            if not agency_year_list:
                missing_years.append(year)

            # filter by race
            agency_year_blk_drv_stops = agency_year.filter(driver_race='Black')
            agency_year_wh_drv_stops = agency_year.filter(driver_race='White')
            agency_year_latino_drv_stops = agency_year.filter(driver_race='Hispanic')
            agency_year_asian_drv_stops = agency_year.filter(driver_race='Asian')
            agency_year_na_drv_stops = agency_year.filter(driver_race='Native American')
            agency_year_nhpi_drv_stops = agency_year.filter(driver_race='Native Hawaiian/Pacific Islander')
            # append
            row['chart_time_series'].append(
                OrderedDict({'year':shorten_year(year),
                'latino_drv_stops':len(agency_year_latino_drv_stops),
                'wh_drv_stops':len(agency_year_wh_drv_stops),
                'blk_drv_stops':len(agency_year_blk_drv_stops),
                'na_drv_stops':len(agency_year_na_drv_stops),
                'nhpi_drv_stops':len(agency_year_nhpi_drv_stops),
                'asian_drv_stops':len(agency_year_asian_drv_stops),
                'total_stops':len(agency_year_list)
                })
            )
        # latest data
        row['big_numbers'] = {}
        max_year = max([x['year'][-2:] for x in row['chart_time_series']])
        # think about how we're abbreviating years here
        agency_latest = agency.stop_set.filter(year=int('20' + max_year))
        row['big_numbers']['year'] = max_year
        row['big_numbers']['stops'] = len(agency_latest)
        row['big_numbers']['searches'] = len(agency_latest.filter(search_conducted=True))
        row['big_numbers']['citations'] = len(agency_latest.filter(outcome='Citation'))
        # demographics
        row['demographics'] = agency.adult_pop_by_race()

        # missing years
        row['missing_years'] = missing_years_text(agency_name,missing_years)

        # copy block on Black driver trends
        copy = build_copy(row)
        row['copy_block'] = copy

        print(row)
        # everything is missing, this is a garbage row
        if len(missing_years) == len(years):
            print('no data found for',agency.name)
            continue
        
        # append row to data
        dupes = [x for x in data if x['name'] == agency_name]
        if dupes:
            print('dupe:',agency.name)
        data.append(row)
    
    # return
    return data


def build_copy(agency_data):
    """
    avg num of stops each year
    chg in pct of Black drivers stopped
    """
    # copy placeholder
    copy = ''
    comparison_text = ''

    # easy access to time series data
    time_series = agency_data['chart_time_series']

    time_series_complete = [x for x in time_series if x['total_stops']]
    
    # nothing to see here
    if not time_series_complete:
        return

    # medians are better than averages because incompleteness
    median_stops = statistics.median([x['total_stops'] for x in time_series_complete]) if time_series_complete else None
    # format thousands separator
    median_stops_f = f"{median_stops:,}" if median_stops else None

    # what's the earliest year on file?
    min_year = min([x['year'] for x in time_series_complete if x['total_stops']])
    # and the latest?
    max_year = max([x['year'] for x in time_series_complete if x['total_stops']])
    # black drivers, total stops for earliest year
    earliest_black_driver_stops, earliest_total_stops = [(x['blk_drv_stops'],x['total_stops']) for x in time_series if x['year'] == min_year][0]
    # black drivers, total stops for latest year
    latest_black_driver_stops, latest_total_stops = [(x['blk_drv_stops'],x['total_stops']) for x in time_series if x['year'] == max_year][0]
    # get pcts for earliest and latest
    earliest_pct_black_driver_stops = round(earliest_black_driver_stops/earliest_total_stops*100,1) 
    latest_pct_black_driver_stops = round(latest_black_driver_stops/latest_total_stops*100,1) 
    # compare earlier to later, taking the first true condition
    if abs(latest_pct_black_driver_stops - earliest_pct_black_driver_stops) < 1:
        comparison_text = 'stayed about the same'
    if latest_pct_black_driver_stops > earliest_pct_black_driver_stops:
        comparison_text = 'increased'
    elif earliest_pct_black_driver_stops > latest_pct_black_driver_stops:
        comparison_text = 'decreased'
    
    # agency name
    agency_name = agency_data['name']

    # mention if the earliest year was the first year
    full_min_year = '20' + min_year.replace("'","")
    min_year_qualified = full_min_year if full_min_year != "2004" else '2004, the first year the state began collecting data' 

    ### COPY SECTION ###
    copy = """{agency} started participating in the Illinois Traffic Stop Study in {minyear}. """.format(
        minyear=min_year_qualified,
        agency=agency_name)
    if median_stops_f:
        copy+="""The median number of annual traffic stops is {medianstops}. """.format(medianstops=median_stops_f)    
    # don't include if the latest pct of black drivers stopped is below 5%
    # also don't include if the first year and last year are the same
    # or if fewer than 50 black drivers are stopped
    if min_year != max_year and latest_black_driver_stops > 50 and latest_pct_black_driver_stops >= 5:
        copy += """The percentage of drivers stopped who are Black has {comparisontext} from {earliestpctblk} in {earliestyear} to {latestpctblk} in {latestyear}.""".format(
                comparisontext=comparison_text,
                earliestpctblk=str(earliest_pct_black_driver_stops)+'%',
                earliestyear="20" + str(min_year).replace("'",""), 
                latestpctblk=str(latest_pct_black_driver_stops)+'%',
                latestyear="20" + str(max_year).replace("'","")
                )
    
    # return what's been compiled
    return copy



def writeout(data):
    # write out    
    outfile = open(outfile_path,'w')
    outjson = json.dump(data,outfile)
    outfile.close()



def roll_thru():
    # debug mode means we don't bother getting statewide
    statewide = get_statewide() if not debug else None
    agencies = get_agencies()
    data = statewide + agencies if statewide else agencies
    writeout(data)

