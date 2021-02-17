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