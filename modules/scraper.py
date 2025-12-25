import requests
from bs4 import BeautifulSoup
import math

# from modules.db_handler import add_internship

def run():    
    #test url
    targetURL = "https://www.linkedin.com/jobs/search/?currentJobId=4346263386&origin=JOBS_HOME_JYMBII"
    session = requests.Session()
    session.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"})
    
    res = session.get(targetURL)
    soup = BeautifulSoup(res.text, 'html.parser')

    element = soup.find("span", class_="results-context-header__job-count")
    # joblist = soup.find("span", id_="ember173")
    total_jobs_found = int("".join([_ for _ in element]).replace(",","").replace("+",""))
    print(total_jobs_found)
    # 25 jobs are listed at a time per page so we have to iterate through 25 listings at a time, if we divide 25 by the total number of jobs found (total_jobs_found) we get how many pages we have in total
    page_loops = math.ceil(total_jobs_found/25)
    # for i in range(page_loops):
    # jobs_on_page = soup.find_all("li") 

    # for j in range(len(jobs_on_page)):
        # jobid = jobs_on_page[j].get("data-occludable-job-id")
        # if jobid is not None:
            # print(jobid)


run()