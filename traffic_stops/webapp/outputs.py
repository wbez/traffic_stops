from django.core import serializers
from stops.models import Stop, Agency
import json

############
# AGENCIES #
############

# setup output file
output_file = open('/home/matt/scratch/mk_test_data_rig/src/content/trafficstops/agencies.json','w')

# get db data
agencies = Agency.objects.all()
data = serializers.serialize('json',agencies)
jdata = [x['fields'] for x in json.loads(data)]

#import ipdb; ipdb.set_trace()

# write out 
json.dump(jdata,output_file)
output_file.close()
