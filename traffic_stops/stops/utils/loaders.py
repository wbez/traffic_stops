import csv, pprint
from traffic_stops.settings import BASE_DIR 
import datetime, dateparser

### START CONFIG ###
data_dir = str(BASE_DIR) + '/data/'
all_infile_names = ['2021 Traffic Data Redacted.txt',
                    '2020 Traffic Data Redacted.txt',
                    '2019_ITSS_Statewide_Redacted.txt',
                    '2018 ITSS Data.txt',
                    '2017 ITSS Data.txt',
                    '2016 ITSS Data.txt',
                    '2015 ITSS Data.txt',
                    '2014 ITSS Data.txt',
                    '2013 ITSS Data.txt',
                    '2012 ITSS Data.txt',
                    '2011 ITSS Data.txt',
                    '2010 ITSS Data.txt',
                    '2009 Raw Data Statewide.txt',
                    '2008 Raw Data Statewide.txt',
                    '2007 Raw Data Statewide without Chicago.txt',
                    '2006 Raw Data Statewide.txt',
                    '2005 Raw Data Statewide.txt',
                    '2004 Raw Data Statewide.txt'] 
### END CONFIG ###

def get_all_headers():
    fieldnames = []
    for filename in all_infile_names:
        filepath = data_dir + filename
        infile = open(filepath)
        incsv = csv.DictReader(infile,delimiter='~')
        print(filename)
        for header in incsv.fieldnames:
            if header not in fieldnames:
                fieldnames.append(header)
                print(header)
        print('~~~')
    pprint.pprint(fieldnames)


def convert_date(date):
    try:
        return dateparser.parse(date)
    except Exception as e:
        print(date,e)
        import ipdb; ipdb.set_trace()


def convert_time(time, row):
    try:
        return datetime.datetime.strptime(time,'%H:%M').time()
    except Exception as e:
        # seeing a lot of '12/30' which maybe we ought to str.replace('/',':')
        print(time,e,row)


def convert_duration(duration):
    try:
        return int(duration)
    except Exception as e:
        print(duration,e)


def convert_int(value,counter):
    try:
        return int(float(value))
    except Exception as e:
        print(counter,value,e)


def get_year(date_obj):
    # TODO optimize this by taking year string for years where
    # format = YYYY-MM-DD
    return date_obj.strftime('%Y')
