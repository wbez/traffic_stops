import csv
from django.db import connection
from stops.models import Stop, Agency
from traffic_stops.settings import BASE_DIR
from reports.utils import get_rate

# google apis
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# google setup
#creds, _ = google.auth.default()
creds = Credentials.from_authorized_user_file('/home/matt/.creds/google.json')
service = build("drive","v3",credentials=creds)
# where all folders, data etc. are stored
root_drive_folder_id = '1DHRLVIRtdAjVl46JygmMliwQE6KC66fp'
# gonna link to this later
# OLD readme_id = '1b4CRyTMIDK9uOuIvNB-WucIdrIwbHahT'
readme_id = '1Yk1J9SAPfZXfYk2Kb-z6K4p4eU6Rhnoc0RciRscymgY'


### START CONFIGS ###
# output
outfile_dir = str(BASE_DIR) + '/reports/output/'
stop_headers = list(Stop.objects.first().__dict__.keys())[1:]
# metadata
agency_codes = [x['code'] for x in Agency.objects.values('code').distinct()]
# update years - ranges don't include last number
years = [x for x in range(2004,2023)] # TODO: mix/max from db
# db stuff
cursor = connection.cursor()
#race_categories = ['White','Hispanic','Black','Native Hawaiian/Pacific Islander','Asian','Native American']
race_categories = [x['driver_race'] for x in Stop.objects.values('driver_race').distinct() if x['driver_race']]
### END CONFIGS ###


def write_out(name,data):
    """
    create file {name}
    using {data} for rows 
    and {data} keys for headers
    """
    output_folder = outfile_dir
    output_path = outfile_dir + name + '.csv'
    headers = data[0].keys()
    output_file = open(output_path,'w')
    output_csv = csv.DictWriter(output_file,headers)
    output_csv.writeheader()
    output_csv.writerows(data)
    output_file.close()
    print('writing out to', output_path)


def agencies_report(year=None):
    """
    each agency's stops, searches, citations
    by race
    together in one csv
    """
    # will write this to spreadsheet
    data = []
    # loop through
    for agency in Agency.objects.all():
        # main query is all agency stops
        stops = agency.stop_set.all()
 
        # filter by year if provided
        if year:
            stops = stops.filter(year=year)
       
        # stops
        black_driver_stops = stops.filter(driver_race='Black')
        white_driver_stops = stops.filter(driver_race='White')
        latino_driver_stops = stops.filter(driver_race='Hispanic')
        
        # searches
        black_driver_searches = black_driver_stops.filter(search_conducted=True)
        white_driver_searches = white_driver_stops.filter(search_conducted=True)
        latino_driver_searches = latino_driver_stops.filter(search_conducted=True) 
       
        # consent searches
        black_driver_consent_searches = black_driver_stops.filter(consent_search_conducted=True)
        white_driver_consent_searches = white_driver_stops.filter(consent_search_conducted=True)
        latino_driver_consent_searches = latino_driver_stops.filter(consent_search_conducted=True) 

        # dog searches
        black_driver_dog_searches = black_driver_stops.filter(dog_search_conducted=True)
        white_driver_dog_searches = white_driver_stops.filter(dog_search_conducted=True)
        latino_driver_dog_searches = latino_driver_stops.filter(dog_search_conducted=True) 
        
        # search hits
        black_driver_search_hits = black_driver_stops.filter(search_hit=True)
        white_driver_search_hits = white_driver_stops.filter(search_hit=True)
        latino_driver_search_hits = latino_driver_stops.filter(search_hit=True)

        # tickets
        black_driver_tickets = black_driver_stops.filter(outcome='Citation')
        white_driver_tickets = white_driver_stops.filter(outcome='Citation')
        latino_driver_tickets = latino_driver_stops.filter(outcome='Citation')
        
        # add stuff to csv row
        row = {
                'Agency':agency.name,
                'Total stops': stops.count(),
                'Black driver stops': black_driver_stops.count(),
                'White driver stops': white_driver_stops.count(),
                'Latino driver stops': latino_driver_stops.count(),
                'Black driver searches': black_driver_searches.count(),
                'White driver searches': white_driver_searches.count(),
                'Latino driver searches': latino_driver_searches.count(),
                'Black driver search rate': get_rate(black_driver_searches.count(),black_driver_stops.count()),
                'White driver search rate': get_rate(white_driver_searches.count(),white_driver_stops.count()),
                'Latino driver search rate': get_rate(latino_driver_searches.count(),latino_driver_stops.count()),
                'Black driver consent search rate': get_rate(black_driver_consent_searches.count(),black_driver_stops.count()),
                'White driver consent search rate': get_rate(white_driver_consent_searches.count(),white_driver_stops.count()),
                'Latino driver consent search rate': get_rate(latino_driver_consent_searches.count(),latino_driver_stops.count()),
                'Black driver dog search rate': get_rate(black_driver_dog_searches.count(),black_driver_stops.count()),
                'White driver dog search rate': get_rate(white_driver_dog_searches.count(),white_driver_stops.count()),
                'Latino driver dog search rate': get_rate(latino_driver_dog_searches.count(),latino_driver_stops.count()),
                'Black driver search hit rate': get_rate(black_driver_search_hits.count(),black_driver_stops.count()),
                'White driver search hit rate': get_rate(white_driver_search_hits.count(),white_driver_stops.count()),
                'Latino driver search hit rate': get_rate(latino_driver_search_hits.count(),latino_driver_stops.count()),
                'Black driver ticket rate': get_rate(black_driver_tickets.count(),black_driver_stops.count()),
                'White driver ticket rate': get_rate(white_driver_tickets.count(),white_driver_stops.count()),
                'Latino driver ticket rate': get_rate(latino_driver_tickets.count(),latino_driver_stops.count())
                }
        # add more stuff
        row['Black and white search rates?'] = 1 if row['Black driver search rate'] and row['White driver search rate'] else 0
        row['Black drivers searched more than white?'] = 1 if row['Black and white search rates?'] and row['Black driver search rate'] > row['White driver search rate'] else 0


        row['Black and white hit rates?'] = 1 if row['Black driver search hit rate'] and row['White driver search hit rate'] else 0
        row['Black driver hit rate lower than white?'] = 1 if row['Black and white hit rates?'] and row['Black driver search hit rate'] < row['White driver search hit rate'] else 0
        
        data.append(row)
        print(row['Agency'])

    # write out
    timeframe = str(year) if year else 'all_years'
    write_out('agency_report_' + timeframe,data)



def agency_export(upload=False):
    """
    for each agency,
    export all their stop data
    to a csv.
    optionally upload to gdrive
    """
    # log uploads
    if upload:
        print('***upload=true will update agency.public_drive_id***')
        logger_file = open('drive_log.csv','w')
        logger_csv = csv.DictWriter(logger_file,['name','file_id','folder_id'])
        logger_csv.writeheader()


    for agency in Agency.objects.all():
        data = Stop.objects.raw("select * from stops where AgencyCode='" + str(agency.code) + "'") 
        outfile_path = outfile_dir + agency.name + '.csv'
        outfile = open(outfile_path,'w')
        outcsv = csv.DictWriter(outfile,stop_headers)
        outcsv.writeheader()
        for row in data.iterator():
            # remove extraneous metadata fields
            row.__dict__.pop('_state')
            row.__dict__.pop('Agency_id')
            # write row as dict
            outcsv.writerow(row.__dict__)
        outfile.close()
        print(outfile_dir,'written')
        if upload:
            print('uploading',agency.name)
            metadata = upload_file(outfile_path)
            file_id, folder_id = metadata['file_id'], metadata['folder_id']
            agency.public_drive_file_id = file_id
            agency.public_drive_folder_id = folder_id
            agency.save()
            logger_csv.writerow({'name':agency.name,'file_id':file_id, 'folder_id': folder_id})

    if upload:
        logger_file.close()



def upload_file(path):
    """
    uploads a file to gdrive
    https://developers.google.com/drive/api/guides/manage-uploads
    """
    # file name is at the end of the path
    file_name = path.split('/')[-1]
    # folder name is file name without extension
    folder_name = file_name.split('.')[0] + ' traffic stops'
    folder_id = create_folder(folder_name)
    # add a readme to the folder
    readme_shortcut(folder_id)

    # start on the data file
    file_metadata = {"name":file_name,"parents":[folder_id]}
    
    # upload 
    # TODO: handle large uploads timing out ...
    try:
        media = MediaFileUpload(path,mimetype="text/csv")
        file = (service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
            )
        file_id = file.get('id')
        service.permissions().create(fileId=file.get('id'),
            body={'type':'anyone','role':'reader'}).execute()
    
        # print and return
        print(file_name,'uploaded with file id',file_id,'to folder name',folder_name,'with folder id',folder_id)
    except Exception as e:
        print(e)
        file_id = None


    return {'file_id':file_id,'folder_id':folder_id}


def create_folder(folder_name):
    """
    each agency gets its own public google drive folder
    to store data + readme files
    https://developers.google.com/drive/api/guides/folder
    """
    # create the folder (calling it a file) and get the id
    file_metadata = {
            'name': folder_name,
            'parents': [root_drive_folder_id],
            'mimeType': 'application/vnd.google-apps.folder',}
    file = service.files().create(body=file_metadata,fields="id").execute()
    file_id = file.get('id')
    # read-only to the world
    service.permissions().create(fileId=file_id,
            body={'type':'anyone','role':'reader'}).execute()

    print(folder_name,file_id)
    return file_id


def readme_shortcut(folder_id):
    """
    https://developers.google.com/drive/api/guides/shortcuts#create-shortcut
    """
    shortcut_metadata = {
            'Name':'readme.txt',
            'mimeType': 'application/vnd.google-apps.shortcut',
            'shortcutDetails': {
                'targetId': readme_id
                },
            'parents':[folder_id]
            }
    try:
        shortcut = service.files().create(body=shortcut_metadata,fields='id').execute()
    except Exception as e:
        print(e)
        print('%%% shortcut exception %%%')

def stops_searches_citations_by_race(agency_codes=None,year=None):
    """
    total stops, searches, citations
    by race
    """
    # queries
    stops_q = "select count(*) from stops where driver_race = %s"
    if agency_codes:
        codes_string = ','.join([str(x) for x in agency_codes])
        stops_q += " and AgencyCode in (" + codes_string +")"
    if year:
        stops_q += 'and year =' + str(year)
    searches_q = stops_q + " and search_conducted = 1"
    citations_q = stops_q + " and outcome = 'Citation'"
    # data to return
    data = {
            'stops':{},
            'searches':{},
            'citations':{}
            }
    # stops
    for race in race_categories:
        data['stops'][race] = cursor.execute(stops_q,[race]).fetchone()[0]
    # searches
    for race in race_categories:
        data['searches'][race] = cursor.execute(searches_q,[race]).fetchone()[0]
    # citations
    for race in race_categories:
        data['citations'][race] = cursor.execute(citations_q,[race]).fetchone()[0]
    # totals and pcts by category
    for cat in data:
        data[cat]['total'] = sum([data[cat][race] for race in race_categories])
    # return
    return data


def ssc_over_time(agency_codes=None,writeout=True):
    """
    a wrapper for stops_searches_citations_by_race
    that iterates over every year 
    and outputs csv
    """
    # collect data from stops_searches_citations_by_race()
    year_data = []
    for year in years:
        print(year)
        data = stops_searches_citations_by_race(agency_codes=agency_codes,year=year)
        data['year'] = year
        year_data.append(data)
    
    # writeout
    if writeout:
        try:
            headers = ['year']
            # get stop categories from data keys, except year
            stop_categories = [x for x in year_data[0] if x!= 'year']
            # splice together header categories, minus year, plus totals
            for race in race_categories + ['total']:
                for stop_category in stop_categories:
                    headers.append(race + '_driver_' + stop_category)
            # only adds agency name if an agency code was specified
            agency_names = ''
            if agency_codes:
                agency_names = '-' + '-'.join([x['AgencyName'] for x in Stop.objects.filter(AgencyCode__in=agency_codes).values('AgencyName').distinct()])
            # setup output file
            outfile_path = outfile_dir + 'ssc_over_time' + agency_names + '.csv'
            outfile = open(outfile_path,'w')
            outcsv = csv.DictWriter(outfile,headers)
            outcsv.writeheader()

            # write data
            for year in year_data:
                row_data = {'year':year['year']}
                # restructure rows
                for category in stop_categories:
                    for race in year[category]:
                        row_data[race + '_driver_' + category] = year[category][race]
                outcsv.writerow(row_data)
            # close file
            outfile.close()
        except Exception as e:
            print(e)
            import ipdb; ipdb.set_trace()
    # return
    return year_data



def outside_chicago():
    for year in range(2004,2023):
        non_chi_stops = Stop.objects.filter(year=year).exclude(AgencyName='CHICAGO POLICE')
        blk_non_chi_stops = non_chi_stops.filter(driver_race='Black')
        print(year,len(non_chi_stops),len(blk_non_chi_stops),len(blk_non_chi_stops)/round(float(len(non_chi_stops)),2))

def more_blk_drivers_stopped_than_pop():
    watchlist = []
    for agency in Agency.objects.all():
        total_stops = len(agency.stop_set.filter(year=2022))
        if len(agency.stop_set.filter(year=2022,driver_race='Black')) and agency.black_nh and len(agency.stop_set.filter(year=2022,driver_race='Black')) > agency.black_nh:
            print(agency.name, total_stops, len(agency.stop_set.filter(year=2022,driver_race='Black')), agency.black_nh)
            watchlist.append((agency.name, total_stops, len(agency.stop_set.filter(year=2022,driver_race='Black')), agency.black_nh))
    print(len(watchlist))
    return watchlist


def black_vs_white_driver_nonmoving_rates():
    """
    returns pcts of black drivers stopped for nonmoving
    vs pct of white drivers stopped for nonmoving
    """
    stops22 = Stop.objects.filter(year=2022)
    blk_drv_stops22 = stops22.filter(driver_race='Black')
    wht_drv_stops22 = stops22.filter(driver_race='White')
    blk_drv_nonmoving=blk_drv_stops22.exclude(ReasonForStop='1')
    wht_drv_nonmoving=wht_drv_stops22.exclude(ReasonForStop='1')
    len(blk_drv_nonmoving)/len(blk_drv_stops22), len(wht_drv_nonmoving)/len(wht_drv_stops22)
    #[Out]# (0.5454437505998169, 0.3622251556700152)


def consent_searches():
    for year in range(2004,2023):
        stops = Stop.objects.filter(year=year)
        black_driver_stops = stops.filter(driver_race='Black')
        white_driver_stops = stops.filter(driver_race='White')
        consents = stops.filter(consent_search_conducted=True)
        white_driver_consents = consents.filter(driver_race='White')
        black_driver_consents = consents.filter(driver_race='Black')
        print(year,len(stops),len(black_driver_stops),len(consents),len(black_driver_consents))


def consent_searches_2022():
    stops = Stop.objects.filter(year=2022)
    black_driver_stops = stops.filter(driver_race='Black')
    white_driver_stops = stops.filter(driver_race='White')
    consents = stops.filter(consent_search_conducted=True)
    black_driver_consents = consents.filter(driver_race='Black')
    white_driver_consents = consents.filter(driver_race='White')
    print(len(black_driver_consents)/len(black_driver_stops),len(white_driver_consents)/len(white_driver_stops))

