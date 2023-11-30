# Generated by Django 4.1 on 2023-11-28 21:04

from django.db import migrations
import re, pdftotext, csv
from traffic_stops.settings import data_dir
from stops.models import Agency


def update_names(apps,schema_editor):
    agency_name_extraction()
    another_agency_name_extraction()

def agency_name_extraction():
    """
    this data was OCR'd via tabula from the 2020 executive summary
    """
    input_data_path = data_dir + 'agency_data_from_2020_exec_summ.csv'
    data = csv.DictReader(open(input_data_path))
    for row in data:
        agency = Agency.objects.get(code=row['ID'])
        agency.regions = row['Regions']
        agency.name_cased = row['Agency'].replace('\n',' ')
        print(agency.name_cased,'has regions',agency.regions)
        agency.save()

def another_agency_name_extraction():
    """
    more agency names that we found elsewhere in some IDOT pdfs
    THIS DOESN'T WORK WELL WHEN AN AGENCY NAME WRAPS A LINE SO WE WORK AROUND THAT
    extracts agency names from this table
    https://idot.illinois.gov/content/dam/soi/en/web/idot/documents/transportation-system/reports/safety/traffic-stop-studies/final--part-i-executive-summary-traffic--6-30-23.pdf#page=62
    """
    pdf_name = 'final--part-i-executive-summary-traffic--6-30-23.pdf'
    pdf_path = data_dir + pdf_name
    pdf = pdftotext.PDF(open(pdf_path,'rb'),physical=True)

    # we're looking for a five-digit sequence
    agency_code_pattern = r"\d{5}"
    before_agency_code_pattern = r"^(.*?)\d{5}"
    before_agency_code_pattern = r"(.*?)(?=\d{5})"

    for page in range(62,96): # pages where the table runs
        # get this page
        pdf_page = pdf[page]
        for line in pdf_page.split('\n'):
            # check if it has an agency code
            compiled_search = re.compile(agency_code_pattern).search(line)
            if compiled_search:
                agency_code = compiled_search.group()
                agency_name = re.match(before_agency_code_pattern, line).group(1).strip()
                agency = Agency.objects.get(code=agency_code)
                # workaround
                if not agency.name_cased:
                    # prevents us from assigning a truncated name
                    if len(agency.name) == len(agency_name):
                        agency.name_cased = agency_name.replace('\n',' ')
                        print(agency.name, agency_name)
                #agency.name_cased = agency_name
                        agency.save()

class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0019_reload_census_w_decennial'),
    ]

    operations = [
            migrations.RunPython(update_names)
    ]
