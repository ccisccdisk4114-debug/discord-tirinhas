import requests
from bs4 import BeautifulSoup
import os


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://www.gocomics.com/garfield"


def pegar_tirinha():

    resposta = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    soup = BeautifulSoup(
        resposta.text,
        "html.parser"
    )

    imagem = soup.find(
        "meta",
        property="og:image"
    )

    if imagem:
        return imagem["content"]

    return None



def enviar_discord(imagem):

    requests.post(
        WEBHOOK,
        json={
            "embeds": [
                {
                    "title": "Tirinha do dia",
                    "image": {
                        "url": imagem
                    }
                }
            ]
        }
    )


tirinha = pegar_tirinha()

if tirinha:
    enviar_discord(tirinha)
else:
    print("Não foi possível encontrar a tirinha")
