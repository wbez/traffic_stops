import json
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
### END CONFIG ###
    
# collect data
data = []

def shorten_year(year):
    return "'" + str(year)[-2:]


def missing_years_text(name,years):
    base = 'IDOT has no traffic stops on file for ' + name.title() + ' in '
    if len(years) == 1:
        return base + str(years[0]) + '.'
    elif len(years) == 2:
        return base + str(years[0]) + ' or ' + str(years[1]) + '.'
    elif len(years) > 2:
        return base + ', '.join([str(x) for x in years[:-1]]) + ' or ' + str(years[-1]) + '.'



# statewide first
row = {'name': 'Illinois statewide','chart_time_series':[]}


# every year
for year in years:
    print('statewide',year)
    # filter by year
    statewide_year = Stop.objects.filter(year=year)

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
            })
        )
print('statewide 2022')
# 2022 data
row['big_numbers'] = {}
statewide_22 = Stop.objects.filter(year=2022)
row['big_numbers']['stops'] = len(statewide_22)
row['big_numbers']['searches'] = len(statewide_22.filter(search_conducted=True))
row['big_numbers']['citations'] = len(statewide_22.filter(outcome='Citation'))
row['demographics'] = illinois_demo_pcts
data.append(row)

# loop thru each agency
for agency in Agency.objects.all():
    # keep track
    missing_years = []

    # set up row
    row = {'name':agency.name.title(),'chart_time_series':[]}
    # loop through each year
    for year in years:
        # filter by year
        agency_year = agency.stop_set.filter(year=year)
        if not list(agency_year):
            missing_years.append(year)

        # filter by race
        agency_year_blk_drv_stops = agency_year.filter(driver_race='Black')
        agency_year_wh_drv_stops = agency_year.filter(driver_race='White')
        agency_year_latino_drv_stops = agency_year.filter(driver_race='Hispanic')
        agency_year_asian_drv_stops = agency_year.filter(driver_race='Asian')
        agency_year_na_drv_stops = agency_year.filter(driver_race='Native American')
        agency_year_nhpi_drv_stops = agency_year.filter(driver_race='Native Hawaiin/Pacific Islander')
        # append
        row['chart_time_series'].append(
            OrderedDict({'year':shorten_year(year),
            'latino_drv_stops':len(agency_year_latino_drv_stops),
            'wh_drv_stops':len(agency_year_wh_drv_stops),
            'blk_drv_stops':len(agency_year_blk_drv_stops),
            'na_drv_stops':len(agency_year_na_drv_stops),
            'nhpi_drv_stops':len(agency_year_nhpi_drv_stops),
            'asian_drv_stops':len(agency_year_asian_drv_stops),
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
    row['missing_years'] = missing_years_text(agency.name,missing_years)

    print(row)
    data.append(row)

# write out    
outfile = open(outfile_path,'w')
outjson = json.dump(data,outfile)
outfile.close()
