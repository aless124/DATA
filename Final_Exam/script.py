import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import re
import csv

def scraping():
    Datas = []
    FullData = []
    
    for i in tqdm(range(1,256)):
        url = "https://www.japscan.me/mangas/"+str(i)
        driver = webdriver.Firefox(executable_path=r'C:\Users\user\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe')
        driver.get(url)
        
        Titles = driver.find_elements(By.CLASS_NAME, "p-2")
        count = 1
        for Title in Titles:
            Origine = "null"
            Statut = "null"
            Age = "null"
            DateSortie = "null"
            Volumes = "null"
            Type = "null"
            Genres = "null"

            url_manga = driver.find_element(By.XPATH, f"/html/body/div[1]/div[2]/div[1]/div/div[3]/div[{count}]/a").get_attribute("href")
            count += 1
            driver2 = webdriver.Firefox(executable_path=r'C:\Users\user\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe')
            driver2.get(url_manga)
            elems = driver2.find_elements(By.CLASS_NAME, "mb-2")
            for elem in elems:
                elem = elem.text
                if ("Nom(s) Alternatif(s):" in elem) or ("Artiste(s):" in elem) or ("Auteur(s):" in elem) or ("Abonnement RSS:" in elem) or ("Nom Original:" in elem) or ("Volumes VF:" in elem):
                    continue
                tempo2 = elem.split(":")
                tempo3 = re.sub('\s+', '', tempo2[1])
                
                if "Origine" in elem:
                    Origine = tempo3
                    
                elif "Statut" in elem:
                    Statut = tempo3

                elif "Âge conseillé" in elem:
                    Age = tempo3

                elif "Volumes VO:" in elem:
                    tempo4 = tempo3.split("(")
                    Volumes = tempo4[0]
                    
                elif "Date Sortie" in elem:
                    DateSortie = tempo3
                
                elif "Type(s)" in elem:
                    Type = tempo3
                
                elif "Genre(s)" in elem:
                    Genres = tempo3

            if Volumes == "null":
                Chap = driver2.find_element(By.CLASS_NAME, "chapters_list")
                tempoChap = Chap.text.split("\n")
                tempoChap2 = tempoChap[1].split(":")
                Volumes = tempoChap2[0][8:]
                print(f"Volumes : {Volumes}")

            image = driver2.find_element(By.TAG_NAME, "img")
            img = image.get_attribute("src")

            Datas = [Title.text, Origine, Statut, Age, DateSortie, Volumes, Type, Genres, img]
            FullData.append(Datas)
            Datas = []
            
            driver2.close()

        driver.close()
    
    # Création du fichier .csv ( pour avoir un tableau lisible sur excel par exemple )
    header = ['Titre', 'Origine', 'Source Statuts', 'Age Rating','Date de sortie','Total Chapter','Type', 'Genres', 'Image']

    with open('Manhua_Test.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(FullData)    


scraping()