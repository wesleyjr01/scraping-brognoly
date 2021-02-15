from bs4 import BeautifulSoup
import requests
import csv
import re

with open("houses_brognoly_20210215.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    houses_urls = list(reader)[0]

house_url = houses_urls[0]
html_text = requests.get(house_url).text
soup = BeautifulSoup(html_text, "lxml")
dormitorios = soup.find("h1", class_="single-property-h1")
dormitorios = dormitorios.text.strip().replace("²", "2 ")

titulo = soup.find("div", {"class": "titulo-imovel"})
titulo = titulo.text.strip()

info = soup.find("ul", {"class": "features gamd-features"}).find_all("li")
for i in info:
    print(i)
    if "bed" in str(i.span):
        comodos = i.div.text.replace("\xa0", "")
        comodos = re.search(r"\d+", comodos).group()
    elif "shower" in str(i.span):
        banheiros = i.div.text.replace("\xa0", "")
        banheiros = re.search(r"\d+", banheiros).group()
    elif "arrows" in str(i.span):
        area_m2 = i.div.text.strip().replace("\xa0", "")
        area_m2 = re.search(r"\d+", area_m2).group()
    elif "car" in str(i.span):
        vagas_garagem = i.div.text.replace("\xa0", "")
        vagas_garagem = re.search(r"\d+", vagas_garagem).group()
    # print("fa fa-bed" in str(i.span))
# print(dormitorios)
# print(titulo)
# print(info)
print(
    {
        "comodos": comodos,
        "banheiros": banheiros,
        "area_m2": area_m2,
        "vagas_garam": vagas_garagem,
    }
)
