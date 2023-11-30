import csv
from stops.models import Agency
from traffic_stops.settings import BASE_DIR 

### START CONFIG ###
outfile_path = str(BASE_DIR) + '/viz/output/cpd_dist_stops_2016-2022.csv'
### END CONFIG ###


cpd = Agency.objects.get(name='CHICAGO POLICE')

cpd16_22 = cpd.stop_set.filter(year__gte=2016)

data = {}

for stop in cpd16_22:
    dist_beat = stop.BeatLocationOfStop
    if len(dist_beat) == 3:
        dist = dist_beat[0]
    elif len(dist_beat) == 4:
        dist = dist_beat[0:2]
    else:
        print(dist_beat)
    dist = int(dist)
    if dist not in data:
        data[dist] = []
    data[dist].append(stop)

outfile = open(outfile_path,'w')
outcsv = csv.DictWriter(outfile,['dist','stops'])
outcsv.writeheader()
for dist in data:
    outcsv.writerow({'dist':dist,'stops':len(data[dist])})
outfile.close()
