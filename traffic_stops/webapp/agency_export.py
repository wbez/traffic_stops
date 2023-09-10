import json
from stops.models import Stop, Agency

### START CONFIG ###
outfile_path = 'webapp/output/agencies.json'
### END CONFIG ###
    
# collect data
data = []

# loop thru each agency
for agency in Agency.objects.all():
    # set up row
    row = {'name':agency.name,'chart_time_series':[]}
    # loop through each year
    for year in range(2004,2023):
        # filter by year
        agency_year = agency.stop_set.filter(year=year)
        # filter by race
        agency_year_blk_drv_stops = agency_year.filter(driver_race='Black')
        agency_year_wh_drv_stops = agency_year.filter(driver_race='White')
        agency_year_latino_drv_stops = agency_year.filter(driver_race='Hispanic')
        agency_year_asian_drv_stops = agency_year.filter(driver_race='Asian')
        agency_year_na_drv_stops = agency_year.filter(driver_race='Native American')
        # append
        row['chart_time_series'].append(
            {'year':year,
            'blk_drv_stops':len(agency_year_blk_drv_stops),
            'wh_drv_stops':len(agency_year_wh_drv_stops),
            'latino_drv_stops':len(agency_year_latino_drv_stops),
            'asian_drv_stops':len(agency_year_asian_drv_stops),
            'na_drv_stops':len(agency_year_na_drv_stops),
            }
        )
    # 2022 data
    row['big_numbers'] = {}
    agency_22 = agency.stop_set.filter(year=2022)
    row['big_numbers']['stops'] = len(agency_22)
    row['big_numbers']['searches'] = len(agency_22.filter(search_conducted=True))
    row['big_numbers']['citations'] = len(agency_22.filter(outcome='Citation'))
    # demographics
    row['demographics'] = agency.driving_age_pop_by_race()

    print(row)
    data.append(row)

# write out    
outfile = open(outfile_path,'w')
outjson = json.dump(data,outfile)
outfile.close()
