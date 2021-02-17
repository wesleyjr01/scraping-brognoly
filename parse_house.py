from bs4 import BeautifulSoup
import requests
import csv
import re
import pandas as pd
from datetime import datetime
import time

with open("houses_urls_brognoly_20210216.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    houses_urls = list(reader)[0]

HOUSES_URLS = houses_urls
TITULO = []
DORMITORIOS = []
COMODOS = []
BANHEIROS = []
AREA_M2 = []
VAGAS_GARAGEM = []
VALOR_IMOVEL = []
IPTU = []
start_time = time.time()
for house in houses_urls:
    print(f"Parsing url: {house}")
    house_url = house
    html_text = requests.get(house_url).text
    soup = BeautifulSoup(html_text, "lxml")

    #
    dormitorios = soup.find("h1", class_="single-property-h1")
    dormitorios = dormitorios.text.strip().replace("²", "2 ")
    dormitorios = re.search(r"\d+", dormitorios).group()

    #
    titulo = soup.find("div", {"class": "titulo-imovel"})
    titulo = titulo.text.strip()

    #
    info = soup.find("ul", {"class": "features gamd-features"}).find_all("li")
    for i in info:
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

    # Valor
    valores = soup.find("div", {"class": "valoresImovel cardEstilo"}).find_all("p")
    valor_imovel = valores[0].text
    try:
        valor_imovel = float(re.search("R\$(\d*.?\d*)", valor_imovel).group(1))
    except:
        valor_imovel = None

    # IPTU
    iptu = valores[1].text
    try:
        iptu = float(re.search("R\$(\d*.?\d*)", iptu).group(1))
    except:
        iptu = None

    # Append values to vectors
    TITULO.append(titulo)
    DORMITORIOS.append(dormitorios)
    COMODOS.append(comodos)
    BANHEIROS.append(banheiros)
    AREA_M2.append(area_m2)
    VAGAS_GARAGEM.append(vagas_garagem)
    VALOR_IMOVEL.append(valor_imovel)
    IPTU.append(iptu)
print(f"{time.time() - start_time} seconds elapsed.")

# Build Dataframe
data_dict = {
    "titulo": TITULO,
    "dormitorios": DORMITORIOS,
    "comodos": COMODOS,
    "banheiros": BANHEIROS,
    "area_m2": AREA_M2,
    "vagas_garagem": VAGAS_GARAGEM,
    "valor_imovel": VALOR_IMOVEL,
    "iptu": IPTU,
}
data = pd.DataFrame.from_dict(data_dict)
now = datetime.now().strftime("%Y%m%d")
data.to_csv(f"dataframe_houses_brognoly_{now}.csv", index=False)