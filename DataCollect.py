import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_linkedin_jobs(pages=5):
    jobs_data = []
    
    for page in range(1, pages+1):
        url=f"https://www.linkedin.com/jobs/search/?keywords=data%20analayst%20jobs%20india&origin=SWITCH_SEARCH_VERTICAL&start={(page-1)*25}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_listings = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        
        for job in job_listings:
            title_element = job.find('h3', class_='base-search-card__title')
            company_element = job.find('h4', class_='base-search-card__subtitle')
            location_element = job.find('span', class_='job-search-card__location')
            
            # Extract job details
            title = title_element.text.strip() if title_element else "N/A"
            company = company_element.text.strip() if company_element else "N/A"
            location = location_element.text.strip() if location_element else "N/A"
            
            # Get the link to the job posting
            link_element = job.find('a', class_='base-card__full-link')
            link = link_element['href'] if link_element else "N/A"
            
            jobs_data.append({
                'Title': title,
                'Company': company,
                'Location': location,
                'Link': link
            })
        
        # Pause to avoid rate limiting
        time.sleep(2)
    
    return jobs_data

# Example usage
data_analyst_jobs = scrape_linkedin_jobs()
df = pd.DataFrame(data_analyst_jobs)
# Save to CSV
df.to_csv('linkedin_data_analyst_jobs.csv', index=False)

# Or save to SQLite database
import sqlite3
conn = sqlite3.connect('linkedin_jobs.db')
df.to_sql('data_analyst_jobs', conn, if_exists='replace', index=False)
conn.close()