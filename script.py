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

# En-têtes HTTP pour simuler un navigateur
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Liste pour stocker toutes les données collectées
all_data = []

# Parcourir chaque URL
for url in urls:
    print(f"Traitement de l'URL : {url}")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Requête réussie pour {url}, analyse des données...")
        soup = BeautifulSoup(response.text, "html.parser")
        data = []

        # Vérifier si le site contient un tableau HTML
        table = soup.find("table")
        if table:
            print("Tableau trouvé, extraction des données en cours...")
            rows = table.find_all("tr")
            for row in rows[1:]:  # Ignorer l'en-tête
                columns = row.find_all("td")
                if columns:
                    # rank = columns[0].text.strip() if len(columns) > 0 else "N/A"
                    company_name = columns[1].text.strip() if len(columns) > 1 else "N/A"
                    # ceo_name = columns[9].text.strip() if len(columns) > 2 else "N/A"
                    # email_tag = columns[11].find("a") if len(columns) > 3 else None
                    # email = email_tag.get("href").replace("mailto:", "").strip() if email_tag else "N/A"
                    # country = columns[4].text.strip() if len(columns) > 4 else "N/A"
                    
                    data.append({
                        # "Rank": rank,
                        "Company Name": company_name,
                        # "CEO Name": ceo_name,
                        # "Email": email,
                        # "Country": country
                    })
        else:
            print("Aucun tableau trouvé, recherche d'autres structures...")
            # Recherche des conteneurs contenant les données (ex. divs, spans)
            containers = soup.find_all("div", class_="organizationName")  # Modifier la classe si nécessaire
            for container in containers:
                # rank = container.find("span", class_="rank").text.strip() if container.find("span", class_="rank") else "N/A"
                company_name = container.find("div", class_="row-cell-value nameField").text.strip() if container.find("div", class_="row-cell-value nameField") else "N/A"
                # ceo_name = container.find("p", class_="ceo-name").text.strip() if container.find("p", class_="ceo-name") else "N/A"
                # email_tag = container.find("a", class_="email")
                # email = email_tag.get("href").replace("mailto:", "").strip() if email_tag else "N/A"
                # country = container.find("span", class_="country").text.strip() if container.find("span", class_="country") else "N/A"
                
                data.append({
                    # "Rank": rank,
                    "Company Name": company_name,
                    # "CEO Name": ceo_name,
                    # "Email": email,
                    # "Country": country
                })

        # Ajouter les données de l'URL actuelle à la liste globale
        all_data.extend(data)
    else:
        print(f"Erreur lors de la requête pour {url} : {response.status_code}")

# Vérifier si des données ont été collectées
if all_data:
    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(all_data)
    # Exporter les données dans un fichier Excel
    df.to_excel("Scraped_Companies_MultipleURLs.xlsx", index=False)
    print("Données exportées avec succès dans 'Scraped_Companies_MultipleURLs.xlsx'.")
else:
    print("Aucune donnée n'a été collectée.")