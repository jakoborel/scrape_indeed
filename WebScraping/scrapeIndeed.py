import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd
import time

# The URL can be adjusted to change the query for jobs

# If comparing in browser, make sure to clear cookies.
# URL = "https://www.indeed.com/q-data-analyst-l-Omaha,-NE-jobs.html"
URL = "https://www.indeed.com/jobs?q=receptionist&l=Omaha%2C+NE"

# request the URL
page = requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")

# print out the pretty html
#print(soup.prettify())

# Extract all job titles from the page
def extract_job_title_from_result(soup):
    jobs = []
    for h2 in soup.find_all(name="h2", attrs={"class":"title"}):
        for a in h2.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return(jobs)

print("Jobs:")
print(len(extract_job_title_from_result(soup)))
print(extract_job_title_from_result(soup))

# Extract company name from the page
def extract_company_from_result(soup):
    companies = []
    for div in soup.find_all(name="div", attrs={"class":"sjcl"}):
        company = div.find_all(name="span", attrs={"class":"company"})
        for b in company:
            companies.append(b.text.strip())
    return(companies)

# print("Companies:")
# print(len(extract_company_from_result(soup)))
# print(extract_company_from_result(soup))

# Extract location from the page
def extract_location_from_result(soup):
    locations = []
    for div in soup.find_all(name="div", attrs={"class":"sjcl"}):

        try:
            locations.append(div.find(name="div", attrs={"class":"location"}).text)
            #print("no exception")
        except Exception as e:
            #print(str(e))
            locations.append(div.find(name="span", attrs={"class":"location"}).text)
    return(locations)

# print("Locations:")
# print(len(extract_location_from_result(soup)))
# print(extract_location_from_result(soup))

# Extract salary from the page
def extract_salary_from_result(soup):
    salaries = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        try:
            salaries.append(div.find(name="span", attrs={"class":"salaryText"}).text)
        except:
            salaries.append("NA")
    return(salaries)

# print("Salaries:")
# print(len(extract_salary_from_result(soup)))
# print(extract_salary_from_result(soup))

# Extract summary bullet points from page
def extract_summary_from_result(soup):
    summaries = []
    i=0
    for div in soup.find_all("div", attrs={"class": "row"}):
        for summary in div.find_all("div", attrs={"class":"summary"}):
            for li in summary.find_all("li"):
                if (len(summaries)<=i):
                    summaries.append(str(li.text))
                    # print("Summary appended")
                elif(len(summaries)>i):
                    summaries[i] = summaries[i] + " " + str(li.text)
                    # print("Summary joined")
                # except Exception as e:
                #    print(str(e))
                #   #summaries.append("NA")
        i+=1
        
    return(summaries)

# print("Summaries:")
# print(len(extract_summary_from_result(soup)))
# print(extract_summary_from_result(soup))

# Build url with a search query and optional arguments for location, salary, and page start filters
def build_url(query, location="", salary="", start=""):
    return "http://www.indeed.com/jobs?q=" + "+".join(str(query).split()) + "+" + str(salary) + "&l=" + str(location) + "&start=" + str(start)

print(build_url("data scientist", "Omaha", "$40,000"))

# max_results_per_city = 100
# city_set = ['New+York','Chicago','San+Francisco', 'Austin', 'Seattle', 'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boulder']
# columns = ["city", "job_title", "company_name", "location", "summary", "salary"]
# sample_df = pd.DataFrame(columns = columns)
#scraping code:
# for city in city_set:
#     for start in range(0, max_results_per_city, 10):
#         page = requests.get('http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=' + str(city) + '&start=' + str(start))
#         time.sleep(1)  #ensuring at least 1 second between page grabs
#         soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
#         #specifying row num for index of job posting in dataframe
#         num = (len(sample_df) + 1) 
#         #creating an empty list to hold the data for each posting
#         job_post = [] 
#         #append city name
#         job_post.append(city) 
#         extract each 
#         #appending list of job post info to dataframe at index num
#         sample_df.loc[num] = job_post

#saving sample_df as a local csv file — define your own local path to save contents 
#sample_df.to_csv("~Documents/GitHub/scrape-indeed/IndeedJobPostings.csv", encoding='utf-8')