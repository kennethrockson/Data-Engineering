# importing the necessary modules/packages
import requests
from pathlib import Path
import csv, re

#NYT doesnt parse data by dates properly so i had to parse it myself
def parse_pub_date(url):
  date_pattern = r"\b(\d{4})/(\d{2})/(\d{2})\b"
  # find the date matches in the url
  dates = re.findall(date_pattern, url)
  return dates
  
# setting up the API Key and NYT search for getting response objects
API_KEY= '7sOHDTmX7gn22GA8zwtAHN1B2aIuwi3Y'
base_url= 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
d_sn_filter='document_type:("article")'
fl_tuple=('abstract','web_url','headline')

# a filter query for keywords, api key, document type, parameters for the past decade, and page 
parameters= {
    'q':'data breach',
    'api-key':API_KEY,
    'page':0,
    'fq':d_sn_filter,
    'begin_date':'20130101',
    'end_date':'20231231',
    'fl':fl_tuple
    }

#Send a request to the ur; with parameters
response= requests.get(base_url,params=parameters)
content= response.json()

# store the year the articles was published
data_year_ = []
for i in content['response']['docs']:
  date_list = parse_pub_date(i['web_url'])
  if date_list:
    data_year_.append(date_list[0][0])

# created a for loop through year data and created a dic
hmap = {}
for year in data_year_:
  if year not in hmap:
    hmap[year] = 0
# counts and adds it to the list
  hmap[year] += 1
  #an object to hold the values
breach_data = []
# creating a list comprehension to to update the values from string to int
for key, value in hmap.items():
  breach_data.append([key, value])
# created a new filepath for csv file
file_path="./data.csv"
# opening the csv file, set to write mode
with open(file_path, mode='w', encoding='utf-8', newline='') as csv_file:
#writes in the rows of the csv file
  csv_writer = csv.writer(csv_file)
  for row in breach_data:
    csv_writer.writerow(row)
    
    print(row)