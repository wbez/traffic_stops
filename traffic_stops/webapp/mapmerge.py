import json, os, shutil
from traffic_stops.settings import BASE_DIR

### START CONFIG ###
webapp_dir = str(BASE_DIR) + '/webapp/'
map_dir = webapp_dir + '/maps/'
agencies_filepath = webapp_dir + 'output/agencies.json'
agencies_json = json.load(open(agencies_filepath))
### END CONFIG ###

# start by copying agencies.json
print('backing up agencies.json')
shutil.copyfile(agencies_filepath, agencies_filepath + '.bk')

# keep track of map files here
mapfiles = []

# walk thru map dir and collect files
for root, dirs, files in os.walk(map_dir):
    for file in files:
        mapfiles.append(file)
#import ipdb; ipdb.set_trace()
# walk through agencies, keeping track where you are
counter = 0 
for agency in agencies_json:
    slug_name = agency['name'].lower().replace(' ','-') + '.png'
    map_match = [ x for x in mapfiles if slug_name == x]
    if map_match:
        agencies_json[counter]['map'] = map_match[0]
        print('adding',map_match[0],'to',agency['name'],'record')
    counter += 1

# write out
print('writing out to',agencies_filepath)
output_file = open(agencies_filepath,'w')
json.dump(agencies_json,output_file)
output_file.close()
