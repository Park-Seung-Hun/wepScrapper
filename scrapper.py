import requests
from bs4 import BeautifulSoup


def get_last_pages(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")
    pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_job(html):
    title = html.find("h2",{"class":"mb4"}).find("a")["title"] # 직종
    company, location = html.find("h3",{"class":"fc-black-700"}).find_all("span",recursive=False) # recursive = False는 전부 가져오는걸 방지(첫단계만)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id= html["data-jobid"]

    return {'title': title,'company': company,'location': location, 'apply_link': f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page,url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: page: {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div",{"class":"-job"}) # 일자리 정보가 들어있음

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs        

def get_jobs(word):
    URL = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_pages(URL)
    jobs = extract_jobs(last_page,URL)
    return jobs