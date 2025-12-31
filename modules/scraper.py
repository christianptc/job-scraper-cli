import requests
from . import db_handler

def get_jobs_raw():
    url = "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
    headers = {"X-API-Key": "jobboerse-jobsuche"}

    # Change SEARCH and LOCATION if you want to use this for your own job search
    params = {
        "was": "Werkstudent Software", # change "Entwickler" with what you want to search for
        "wo": "Kiel", # change "Kiel" with the region your prefered region
        "umkreis": 50,
        "page": 1,
        "size": 50, # <- this represents the maximum amount of jobs that can be extracted and stored in the database, try to increase it if you need new ones and can't find new ones.
        "sortierung" : "datum"
    }

    response = requests.get(url, params=params, headers=headers)

    data = response.json()
    raw_jobs = data.get('stellenangebote', [])
    # print(raw_jobs)
    total_new_jobs = 0
    for job in raw_jobs:
        ref_nr = job.get('refnr', None)
        company_name = job.get('arbeitgeber', None)
        position = job.get('titel', job.get('beruf', None))
        location = job.get('arbeitsort', {}).get('ort', None)
        link = job.get('externeUrl', f"https://www.arbeitsagentur.de/jobsuche/jobdetail/{ref_nr}")
        date_posted = job.get('aktuelleVeroeffentlichungsdatum', None)
        
        check = db_handler.add_internship(company_name, position, location, link, date_posted)
        if check:
            total_new_jobs += 1

    return len(raw_jobs), total_new_jobs
    
# get_jobs_raw()