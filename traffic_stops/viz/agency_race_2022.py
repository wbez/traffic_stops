from stops.models import Agency
from traffic_stops.settings import BASE_DIR 
import csv

### START CONFIG ###
output_file_path = str(BASE_DIR) + '/viz/output/agency_race_2022.csv'
### END CONFIG ###


data = []

def pctify(num,den):
    return str(round(num/den*100,2)) + '%' 


for agency in Agency.objects.all():
    # set up row
    row = {'Agency Name': agency.name}
    
    # totals
    agency_stops_22 = agency.stop_set.filter(year=2022)
    stops_22_count = len(agency_stops_22)
    row['Total 2022 stops'] = stops_22_count if stops_22_count else 'NA'
    
    if stops_22_count:
        # by race
        latino = agency_stops_22.filter(driver_race='Hispanic')
        latino_count = len(latino)
        latino_pct = pctify(latino_count,stops_22_count)

        white = agency_stops_22.filter(driver_race='White')
        white_count = len(white)
        white_pct = pctify(white_count,stops_22_count)

        black = agency_stops_22.filter(driver_race='Black')
        black_count = len(black)
        black_pct = pctify(black_count,stops_22_count)

        asian = agency_stops_22.filter(driver_race='Asian')
        asian_count = len(asian)
        asian_pct = pctify(asian_count,stops_22_count)

        naan = agency_stops_22.filter(driver_race='Native American')
        naan_count = len(naan)
        naan_pct = pctify(naan_count,stops_22_count)

        hpi = agency_stops_22.filter(driver_race='Native Hawaiian/Pacific Islander')
        hpi_count = len(hpi)
        hpi_pct = pctify(hpi_count,stops_22_count)

        # build row
        row['Latino'] = latino_pct
        row['White'] = white_pct
        row['Black'] = black_pct
        row['Asian'] = asian_pct
        row['American Indian/Alaska Native'] = naan_pct 
        row['Native Hawaiian/Pacific Islander'] = hpi_pct

    else:
        # nothing to compute if there are no totals
        row['Latino'] = ''
        row['White'] = ''
        row['Black'] = ''
        row['Asian'] = ''
        row['American Indian/Alaska Native'] = ''
        row['Native Hawaiian/Pacific Islander'] = '' 

    # add row to data
    data.append(row)
    print(row)


# set up csv
outfile = open(output_file_path,'w')
outcsv = csv.DictWriter(outfile,data[0].keys())
outcsv.writeheader()
outcsv.writerows(data)
outfile.close()
