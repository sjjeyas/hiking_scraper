import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


URL = "https://www.hikingproject.com/"
page = requests.get(URL)

states = ["https://www.hikingproject.com/directory/8007121/california"]
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="directory-us")
trails = results.find_all("div", class_="onx-directory__item area")


all_links = []
for trail in trails:
    links = trail.find_all("a")
    for link in links:
            link_url = link["href"]
            if link_url in states:
                print(link_url)
                URL = link_url
                page =  requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                state_results = soup.find(id="subareas")
                areas = state_results.find_all("div", class_="area")
                for area in areas:
                    sublocations = area.find_all("a")
                    for sublocation in sublocations:
                        u = sublocation["href"]
                        all_links.append(u)
                        print(u)

all_trails = []

for all_link in all_links:
    URL = all_link
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="area-page")
    trails = results.find_all("tr", class_="trail-row")
    for trail in trails:
        links = trail.find_all("a")
        for link in links:
            link_url = link["href"]
            location = trail.find("div", class_="float-xs-right")
            all_trails.append([link_url, location.text.strip()])
            print(link_url)
            print(location.text.strip())
    
data = []
i = 0          
for all_trail in all_trails:
    URL = all_trail[0]
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    basics = soup.find(id="title-bar")   
    name = basics.find("div", class_="onx-title-bar__title" )
    name = name.text.strip()
    results = soup.find(id="trail-text")
    descriptions = results.find_all("div", "mb-1")
    if 2 < len(descriptions):
        description = descriptions[2].text.strip()
        dbtrail = {
            "name": name,
            "description": description,
            "location": all_trail[1],
        }
        data.append(dbtrail)
        print(f"Appending trail: {dbtrail}")  # Debugging output
        #data.append(dbtrail)
        #print(f"Processed trail {i}: {name}")
        print(i)
        i = i+1
    
with open("ca_trails.json", "w") as outfile:
        json.dump(data, outfile, indent=1)
#print(all_trails)