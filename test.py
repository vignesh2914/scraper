import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
 
#csv file save process
def create_file_path(user_keywords):
    timestamp = datetime.now().strftime("%Y %m %d %H %M %S")
    file_path = f'linkedin-jobs-{user_keywords}-{timestamp}.csv'
    return file_path
 
def linkedin_scraper(webpage, keywords, file_path, page_number):
    next_page = f"{webpage}&keywords={keywords}&start={page_number}"  
    print(next_page)
   
    try:
        response = requests.get(next_page)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Error in request: {e}")
        return
 
    soup = BeautifulSoup(response.content, 'html.parser')
 
    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    for job in jobs:
        job_title = job.find('h3', class_='base-search-card__title').text.strip()
        job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
        job_location = job.find('span', class_='job-search-card__location').text.strip()  
        job_link = job.find('a', class_='base-card__full-link')['href']
 
        with open(file_path, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([job_title, job_company, job_location, job_link])
    print('Data updated')
 
    if page_number < 25:
        page_number += 25
        linkedin_scraper(webpage, keywords, file_path, page_number)
    else:
        print('File closed')
 
user_keywords = input("Enter the job keywords: ")
 
dynamic_url = f'https://www.linkedin.com/jobs/search/?currentJobId=3808377479&distance=25&f_TPR=r86400&geoId=102713980&keywords={user_keywords}&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'
 
file_path = create_file_path(user_keywords)
linkedin_scraper(dynamic_url, user_keywords, file_path, page_number=0)