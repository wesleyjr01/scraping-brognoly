import aiohttp
import asyncio
import ssl
import utils
import csv
import pandas as pd
from datetime import datetime

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


async def fetch(session, url):
    print(f"Fething url: {url}")
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        print("Done url fetching.")
        # return await response.read()
        response_text = await response.read()
        return response_text


async def fetch_all(urls, loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls], return_exceptions=True
        )
        return results


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    urls = houses_urls
    htmls = loop.run_until_complete(fetch_all(urls, loop))
    for html in htmls:
        titulo = utils.extract_titulo(html)
        dormitorios = utils.extract_dormitorios(html)
        comodos = utils.extract_information(html, span_pattern="bed")
        banheiros = utils.extract_information(html, span_pattern="shower")
        area_m2 = utils.extract_information(html, span_pattern="arrows")
        vagas_garagem = utils.extract_information(html, span_pattern="car")
        valor_imovel = utils.extract_valor_imovel(html)
        iptu = utils.extract_iptu(html)

        # update vectors
        TITULO.append(titulo)
        DORMITORIOS.append(dormitorios)
        COMODOS.append(comodos)
        BANHEIROS.append(banheiros)
        AREA_M2.append(area_m2)
        VAGAS_GARAGEM.append(vagas_garagem)
        VALOR_IMOVEL.append(valor_imovel)
        IPTU.append(iptu)

    # Build Dataframe
    data_dict = {
        "url": HOUSES_URLS,
        "titulo": TITULO,
        "dormitorios": DORMITORIOS,
        "comodos": COMODOS,
        "banheiros": BANHEIROS,
        "area_m2": AREA_M2,
        "vagas_garagem": VAGAS_GARAGEM,
        "valor_imovel": VALOR_IMOVEL,
        "iptu": IPTU,
    }

    # Export data to .csv
    data = pd.DataFrame.from_dict(data_dict)
    now = datetime.now().strftime("%Y%m%d")
    data.to_csv(f"dataframe_houses_brognoly_{now}.csv", index=False)