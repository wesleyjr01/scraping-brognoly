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
    # return BeautifulSoup(results.decode("utf-8"), "html5lib")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    urls = houses_urls
    htmls = loop.run_until_complete(fetch_all(urls, loop))
    for html in htmls:
        dormitorios = utils.extract_dormitorios(html)
        DORMITORIOS.append(dormitorios)

    # Build Dataframe
    data_dict = {
        "url": HOUSES_URLS,
        # "titulo": TITULO,
        "dormitorios": DORMITORIOS,
        # "comodos": COMODOS,
        # "banheiros": BANHEIROS,
        # "area_m2": AREA_M2,
        # "vagas_garagem": VAGAS_GARAGEM,
        # "valor_imovel": VALOR_IMOVEL,
        # "iptu": IPTU,
    }

    data = pd.DataFrame.from_dict(data_dict)
    now = datetime.now().strftime("%Y%m%d")
    print(data.head())
    data.to_csv(f"dataframe_houses_brognoly_{now}.csv", index=False)