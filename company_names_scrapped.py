import requests
from bs4 import BeautifulSoup
import pandas as pd

# Liste des URL cibles
urls = [
    "https://growjo.com/industry/AI",
    "https://growjo.com/industry/AI/2",
    "https://growjo.com/industry/AI/3",
    "https://www.forbes.com/lists/ai50/",
]


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


all_data = []

for url in urls:
    print(f"Traitement de l'URL : {url}")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Requête réussie pour {url}, analyse des données...")
        soup = BeautifulSoup(response.text, "html.parser")
        data = []

        table = soup.find("table")
        if table:
            print("Tableau trouvé, extraction des données en cours...")
            rows = table.find_all("tr")
            for row in rows[1:]:  # Ignorer l'en-tête
                columns = row.find_all("td")
                if columns:
                    company_name = columns[1].text.strip() if len(columns) > 1 else "N/A"
                    data.append({
                        "Company Name": company_name,
                    })
        else:
            print("Aucun tableau trouvé, recherche d'autres structures...")
            containers = soup.find_all("div", class_="organizationName")  # Modifier la classe si nécessaire
            for container in containers:
                company_name = container.find("div", class_="row-cell-value nameField").text.strip() if container.find("div", class_="row-cell-value nameField") else "N/A"
                data.append({
                    "Company Name": company_name,
                })

        all_data.extend(data)
    else:
        print(f"Erreur lors de la requête pour {url} : {response.status_code}")
        containers = soup.find_all("div", class_="organizationName")  # Modifier la classe si nécessaire
        for container in containers:
                company_name = container.find("div", class_="row-cell-value nameField").text.strip() if container.find("div", class_="row-cell-value nameField") else "N/A"

if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv("Scraped_Companies_names.csv", index=False)
    print("Données exportées avec succès dans 'Scraped_Companies_MultipleURLs.csv'.")
else:
    print("Aucune donnée n'a été collectée.")
