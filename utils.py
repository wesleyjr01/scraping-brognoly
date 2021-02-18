from bs4 import BeautifulSoup
import re


def extract_dormitorios(text):
    soup = BeautifulSoup(text.decode("utf-8"), "lxml")
    try:
        dormitorios = soup.find("h1", class_="single-property-h1")
        dormitorios = dormitorios.text.strip().replace("²", "2 ")
        dormitorios = re.search(r"\d+", dormitorios).group()
        return dormitorios
    except:
        return None


def extract_titulo(text):
    soup = BeautifulSoup(text.decode("utf-8"), "lxml")
    titulo = soup.find("div", {"class": "titulo-imovel"})
    titulo = titulo.text.strip()
    return titulo


def extract_information(text, span_pattern):
    soup = BeautifulSoup(text.decode("utf-8"), "lxml")
    info = soup.find("ul", {"class": "features gamd-features"}).find_all("li")
    information = None
    for i in info:
        if span_pattern in str(i.span):
            information = i.div.text.replace("\xa0", "")
            information = re.search(r"\d+", information).group()
    return information


def extract_valor_imovel(text):
    soup = BeautifulSoup(text.decode("utf-8"), "lxml")
    valores = soup.find("div", {"class": "valoresImovel cardEstilo"}).find_all("p")
    valor_imovel = valores[0].text
    try:
        valor_imovel = float(re.search("R\$(\d*.?\d*)", valor_imovel).group(1))
    except:
        valor_imovel = None
    return valor_imovel


def extract_iptu(text):
    soup = BeautifulSoup(text.decode("utf-8"), "lxml")
    valores = soup.find("div", {"class": "valoresImovel cardEstilo"}).find_all("p")
    iptu = valores[1].text
    try:
        iptu = float(re.search("R\$(\d*.?\d*)", iptu).group(1))
    except:
        iptu = None
    return iptu