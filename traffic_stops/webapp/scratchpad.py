import csv
from stops.models import Stop, Agency

### START CONFIG ###
agency_name = 'CHICAGO POLICE'
outfile_path = agency_name.replace(' ','-') + '_stops_by_race.csv'
### END CONFIG ###

# get agency
agency = Agency.objects.get(name=agency_name)
    
# collect data
data = []

# loop through each year
for year in range(2004,2023):
    
    agency_year = cpd.stop_set.filter(year=year)
    agency_year_blk_drv_stops = agency_year.filter(driver_race='Black')
    agency_year_wh_drv_stops = agency_year.filter(driver_race='White')
    agency_year_latino_drv_stops = agency_year.filter(driver_race='Hispanic')
    agency_year_asian_drv_stops = agency_year.filter(driver_race='Asian')
    agency_year_na_drv_stops = agency_year.filter(driver_race='Native American')
    data.append(
	    {'year':year,
	    'blk_drv_stops':len(agency_year_blk_drv_stops),
	    'wh_drv_stops':len(agency_year_wh_drv_stops),
	    'latino_drv_stops':len(agency_year_latino_drv_stops),
	    'asian_drv_stops':len(agency_year_asian_drv_stops),
	    'na_drv_stops':len(agency_year_na_drv_stops),
	    }
	    )

# write out    
outfile = open(outfile_path,'w')
outcsv = csv.DictWriter(outfile,data[0].keys())
outcsv.writerows(data)
outfile.close()
