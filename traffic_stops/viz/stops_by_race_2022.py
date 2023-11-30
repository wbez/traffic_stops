from stops.models import Stop
from traffic_stops.settings import BASE_DIR
import csv

### START CONFIG ###
outfile_path = str(BASE_DIR) + '/viz/output/stops_by_race_2022.csv'
### END CONFIG ###

stops22 = Stop.objects.filter(year=2022)
stops22_count = len(stops22)

race_cats = [cat['driver_race'] for cat in stops22.values('driver_race').distinct() if cat['driver_race']]

data = {}

print(race_cats)

for cat in race_cats:
    stops22_by_race = stops22.filter(driver_race=cat)
    stops22_by_race_count = len(stops22_by_race)
    data[cat] = str(round(stops22_by_race_count / stops22_count * 100,2)) + '%'
    print(cat,' : ',data[cat])

# output
outfile = open(outfile_path,'w')
outcsv = csv.DictWriter(outfile,data.keys())
outcsv.writeheader()
outcsv.writerow(data)
outfile.close()

