import requests, json, fiona
from shapely.geometry import shape
from stops.models import Agency
from traffic_stops.settings import BASE_DIR

### START CONFIG ###
template_url = "https://api.mapbox.com/styles/v1/mapbox/light-v11/static/pin-l+ff0000({lat},{lon})/[-91.666,36.6362,-87.053,42.8369]/200x350?access_token=pk.eyJ1IjoiY2t1cmdhbndiZXoiLCJhIjoiY2xtODR5eDZkMDZjazNqbnp6Z2xlcmpzeCJ9.UOjL4Dy56jwCRe75Qc19iw"
shapes_base_path = str(BASE_DIR) + '/webapp/shapes/'
place_shape_file_path = shapes_base_path + 'cb_2022_17_place_500k.shp'
county_shape_file_path = shapes_base_path + 'cb_2022_us_county_500k.shp'
# for outputs
map_path = str(BASE_DIR) + '/webapp/maps/'
### END CONFIG ###


# start with places
place_shapes = fiona.open(place_shape_file_path)
# then counties 
county_shapes = fiona.open(county_shape_file_path)
# iterate
for agency in Agency.objects.all():
    # slugify
    agency_name = agency.name.replace(' ','-').lower()
    # for lookups
    geoid = agency.geoid
    # any and all place, county matches
    place_match = [x for x in place_shapes if x.properties['GEOID'] == geoid]
    county_match = [x for x in county_shapes if x.properties['GEOID'] == geoid]
    # can either match on place or county
    if place_match:
        smatch = place_match[0]
    elif county_match:
        smatch = county_match[0]
    else:
        print('no match for',agency.name,agency.geoid)
        # ope! can't make a map w/o geo information
        continue
    # whatever matched, show it here
    print(agency.name,'matches',smatch.properties['NAME'])
    # make it a shape
    shp_geom = shape(smatch['geometry'])
    # get centroid coords
    lat, lon = shp_geom.centroid.coords[0]
    # make a url
    req_url = template_url.format(lon=lon,lat=lat)
    # req from mapbox
    response = requests.get(req_url)
    # write to a buffer
    map_buffer = open(map_path + agency_name + '.png','wb')
    map_buffer.write(response.content)
    map_buffer.close()
    print('writing map for',agency_name)
