import requests
from bs4 import BeautifulSoup
import os


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://www.gocomics.com/peanuts"


def pegar_tirinha():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    resposta = requests.get(
        URL,
        headers=headers
    )

    soup = BeautifulSoup(
        resposta.text,
        "html.parser"
    )

    # Procura a imagem real da tirinha pelo componente do GoComics
    imagem = soup.find(
        "img",
        class_=lambda x: x and "comic__image" in x
    )

    if imagem:
        return imagem.get("src")

    return None



def enviar_discord(imagem):

    dados = {
        "embeds": [
            {
                "title": "Peanuts - Tirinha do dia",
                "image": {
                    "url": imagem
                },
                "footer": {
                    "text": "Publicado automaticamente pelo Daily Comics"
                }
            }
        ]
    }

    resposta = requests.post(
        WEBHOOK,
        json=dados
    )

    if resposta.status_code != 204:
        print("Erro ao enviar para o Discord:")
        print(resposta.text)



tirinha = pegar_tirinha()


if tirinha:

    print("Tirinha encontrada:")
    print(tirinha)

    enviar_discord(tirinha)

else:

    print("Não foi possível encontrar a tirinha.")
