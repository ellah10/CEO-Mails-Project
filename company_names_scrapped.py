import requests
from bs4 import BeautifulSoup
import pandas as pd

urls = [
    "https://growjo.com/industry/AI",
    "https://growjo.com/industry/AI/2",
    "https://growjo.com/industry/AI/3",
    "https://www.forbes.com/lists/ai50/",
    "https://www.datamation.com/featured/ai-companies/", 
    "https://tracxn.com/d/artificial-intelligence/ai-startups-in-enterprise-software-in-china/__q4JgD1q-ysBg2_1Ln6xU3mLX1Umfce5gM-l2mY8ffks/companies#t-1-agora", 
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

all_data = []

for url in urls:
    print(f" URL processing : {url}")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Successful request for {url}, data analysis...")
        soup = BeautifulSoup(response.text, "html.parser")
        data = []

        table = soup.find("table")
        if table:
            print("Table found, data extraction in progress...")
            rows = table.find_all("tr")
            for row in rows[1:]:
                columns = row.find_all("td")
                if columns:
                    company_name = columns[1].text.strip() if len(columns) > 1 else "N/A"
                    data.append({
                        "Company Name": company_name,
                    })
        else:
            print("No table found, looking for other structures...")

            if "datamation" in url:
                containers = soup.find_all("h3") 
                for container in containers:
                    company_name = container.find("strong")  
                    company_name = company_name.text.strip() if company_name else "N/A"
                    data.append({
                        "Company Name": company_name,
                    })
            elif "tracxn" in url:
                containers = soup.find_all("h2")  # Look for this class to find company names
                for container in containers:
                    company_name = container.find("a")  # The company name is within <h2> tags
                    company_name = company_name.text.strip() if company_name else "N/A"
                    data.append({
                        "Company Name": company_name,
                    })
            else:
                containers = soup.find_all("div", class_="organizationName")
                for container in containers:
                    company_name = container.find("div", class_="row-cell-value nameField").text.strip() if container.find("div", class_="row-cell-value nameField") else "N/A"
                    data.append({
                        "Company Name": company_name,
                    })
        all_data.extend(data)
    else:
        print(f"Error when requesting {url} : {response.status_code}")
        containers = soup.find_all("div", class_="organizationName")
        for container in containers:
            company_name = container.find("div", class_="row-cell-value nameField").text.strip() if container.find("div", class_="row-cell-value nameField") else "N/A"
            all_data.append({
                "Company Name": company_name,
            })

if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv("Scraped_Companies_names.csv", index=False)
    print("Data successfully exported to 'Scraped_Companies_names.csv'.")
else:
    print("No data collected.")
