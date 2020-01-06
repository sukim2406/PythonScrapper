import requests
from bs4 import BeautifulSoup

LIMIT = 50
INDEED_URL = f"https://www.indeed.com/jobs?q=Software+Engineer&l=Lafayette,+IN&radius=100&explvl=entry_level&limit={LIMIT}"

def extract_indeed_pages():
    result = requests.get(INDEED_URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {"class":"pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.find('span').string))
    max_page = pages[-1]

    return max_page


def extract_indeed_components(html):
    #extract job title
    title = html.find("div",{"class": "title"}).find("a")["title"]
    
    #extract company name
    company = html.find("div",{"class": "sjcl"}).find("span",{"class":"company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = (str(company.find("a").string))
    else:
        company = (str(company.string))
    company = company.strip()

    #extract company location
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    #extrac job id
    job_id = html["data-jk"]

    return {
        'title': title, 
        'company': company, 
        'location': location, 
        'link': f"https://www.indeed.com/viewjob?jk={job_id}"
    }


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{INDEED_URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
        for result in results:
            job = extract_indeed_components(result)
            jobs.append(job)
        
    return jobs


def get_jobs():
    last_page = extract_indeed_pages()
    jobs = extract_indeed_jobs(last_page)
    
    return jobs

