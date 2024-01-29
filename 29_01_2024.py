import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time  

# csv file save process
def create_file_path(user_keywords):
    timestamp = datetime.now().strftime("%Y %m %d %H %M %S")
    file_path = f'linkedin-jobs-{user_keywords}-{timestamp}.csv'
    return file_path

def linkedin_scraper(webpage, keywords, file_path, page_number=0):
    while True:
        next_page = f"{webpage}&keywords={keywords}&start={page_number * 25}"
        print(next_page)

        try:
            response = requests.get(next_page)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error in request: {e}")
            return

        if response.status_code == 429:
            print("Rate limit exceeded. Waiting for a while")
            time.sleep(60)  
            continue  

        soup = BeautifulSoup(response.content, 'html.parser')

        jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        if not jobs:
            break  

        for job in jobs:
            job_title = job.find('h3', class_='base-search-card__title').text.strip()

            job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()

            job_location = job.find('span', class_='job-search-card__location').text.strip()

            job_link = job.find('a', class_='base-card__full-link')['href']

            with open(file_path, 'a', encoding='utf-8', newline='') as file:

                writer = csv.writer(file)

                writer.writerow([job_title, job_company, job_location, job_link])

        print('Data updated')

        page_number += 1

user_keywords = input("Enter the job keywords: ")

user_location = input("Enter the location: ")

user_filter = int(input("Enter the value (1-4): "))

job_filter_1_Anytime = f'https://www.linkedin.com/jobs/search/?currentJobId=3810061572&keywords={user_keywords}&location={user_location}&origin=JOB_SEARCH_PAGE_LOCATION_HISTORY&refresh=true'

job_filter_2_PastMonth = f'https://www.linkedin.com/jobs/search/?currentJobId=3799271140&f_TPR=r2592000&keywords={user_keywords}&location={user_location}&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'

job_filter_3_PastWeek = f'https://www.linkedin.com/jobs/search/?currentJobId=3812840127&f_TPR=r604800&keywords={user_keywords}&location={user_location}&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'

job_filter_4_Past_24hr = f'https://www.linkedin.com/jobs/search/?currentJobId=3812840127&f_TPR=r86400&keywords={user_keywords}&location={user_location}&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'


file_path = create_file_path(user_keywords)

if user_filter == 1:
    linkedin_scraper(job_filter_1_Anytime, user_keywords, file_path)

elif user_filter == 2:
    linkedin_scraper(job_filter_2_PastMonth, user_keywords, file_path)

elif user_filter == 3:
    linkedin_scraper(job_filter_3_PastWeek, user_keywords, file_path)

elif user_filter == 4:
    linkedin_scraper(job_filter_4_Past_24hr, user_keywords, file_path)

else:
    print("Invalid filter value. Please enter a value between 1 and 4.")
