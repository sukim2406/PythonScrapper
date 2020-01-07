import requests
from bs4 import BeautifulSoup

STACKOVERFLOW_URL = f"https://stackoverflow.com/jobs?q=software+engineer&ms=Junior&sort=i"

def extract_stackoverflow_pages():
    result = requests.get(STACKOVERFLOW_URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
    last_page =pages[-2].get_text(strip=True)
    return int(last_page)


def extract_stackoverflow_components(html):
    #extract job title
    title = html.find("div", {"class": "grid--cell"}).find("h2").string

    #extract company name & location
    company, location = html.find("div", {"class": "grid--cell"}).find("h3").find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)

    #extract job id
    job_id = html['data-jobid']
    
    return {
        'title': title, 
        'company': company, 
        'location': location,
        'link': f"https://stackoverflow.com/jobs/{job_id}"
    }

def extract_stackoverflow_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{STACKOVERFLOW_URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"-job"})
        for result in results:
            job = extract_stackoverflow_components(result)
            jobs.append(job)
        return jobs


def get_jobs():
    last_page = extract_stackoverflow_pages()
    jobs = extract_stackoverflow_jobs(last_page)
    return jobs