import ray 
import requests
import os
import json
import pandas as pd
from datetime import datetime

ray.init()

# locations to scrape 
@ray.remote
def zillow_scrape_by_location(location):
    zipcode = location
    url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    headers = {
        "X-RapidAPI-Key": "5b4b1b277fmsh1110389d1172efdp110d88jsn1752f5f18426",
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
    }
    
    querystring = {"location": zipcode}
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            results = data['results']
            scraped_data = []
            for result in results:
                address = result.get('address', {}).get('streetAddress')
                price = result.get('price')
                daysOnZillow = result.get('daysOnZillow')
                # Check if all necessary fields are present
                if address and price and daysOnZillow:
                    scraped_data.append({
                        'address': address,
                        'price': price,
                        'daysOnZillow': daysOnZillow
                    }) 
            if scraped_data:
                return scraped_data
        else:
            print("No results found.")
            return None
    else: 
        print(f"Error: {response.status_code} - {response.text}")
        return None

# locations to scrape 
locations = ["Mission TX", "Mcallen TX", "Laredo TX", "Edinburg TX", "Pharr TX"]

# distribute scraping tasks to workers
tasks = [zillow_scrape_by_location.remote(location) for location in locations]
# wait for all tasks to complete
results = ray.get(tasks)

# concatenate results into a single dataframe
all_data = []
for result in results: 
    if result:
        all_data.extend(result)
        
df = pd.DataFrame(all_data)

# print the dataframe to check if it contains any data
print("DataFrame:")
print(df)

# write the dataframe to csv format
file_path = f"/home/azureuser/my_proj/web scraping project/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(file_path, index=False)

# shutdown Ray
ray.shutdown()
