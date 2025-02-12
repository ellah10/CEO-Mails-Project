from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv  # Importation de la bibliothèque csv pour l'exportation


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


url = "https://growjo.com/industry/AI"
driver.get(url)

time.sleep(5)

table = driver.find_element(By.XPATH, '//table')

# Trouver le tableau contenant les informations des entreprises
rows = table.find_elements(By.TAG_NAME, 'tr') # Si le tableau est dans une balise <table>

# Liste pour stocker les données extraites
entreprises = []

# Parcourir chaque ligne du tableau (tr)
for row in table.find_all('tr')[1:]:  # [1:] pour ignorer l'en-tête du tableau
    cols = row.find_all('td')
    
    if len(cols) > 1:
        nom_entreprise = cols[1].get_text(strip=True)
        ceo = cols[9].get_text(strip=True)
        pays = cols[4].get_text(strip=True)

        # Essayer de récupérer l'email si un bouton est présent
        try:
            # Trouver et cliquer sur le bouton pour afficher l'email
            email_button = driver.find_element(By.TAG_NAME, "button")
            email_button.click()
            time.sleep(2)  # Attendre que l'email apparaisse

            # Extraire l'email maintenant qu'il est visible
            email = cols[11].get_text(strip=True)  # Ajuste selon la colonne exacte
        except Exception as e:
            email = "Non disponible"

        # Ajouter les données à la liste des entreprises
        entreprises.append({
            "Nom de l'entreprise": nom_entreprise,
            "CEO": ceo,
            "Pays": pays,
            "Email": email
        })

# Fermer le navigateur après avoir scrappé les données
driver.quit()

# Nom du fichier CSV
csv_file = "entreprises.csv"

# Écrire les données dans un fichier CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Nom de l'entreprise", "CEO", "Pays", "Email"])
    writer.writeheader()  # Écrire l'en-tête (noms des colonnes)
    writer.writerows(entreprises)  # Écrire les données extraites

print(f"Les données ont été exportées dans {csv_file}")