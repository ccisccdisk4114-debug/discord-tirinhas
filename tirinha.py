from playwright.sync_api import sync_playwright
import requests
import os


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://www.gocomics.com/peanuts"


def pegar_tirinha():

    with sync_playwright() as p:

        navegador = p.chromium.launch(
            headless=True
        )

        pagina = navegador.new_page()

        pagina.goto(
            URL,
            wait_until="networkidle"
        )

        # Espera a imagem da tirinha aparecer
        pagina.wait_for_selector(
            "img[class*='comic__image']"
        )

        imagem = pagina.locator(
            "img[class*='comic__image']"
        ).first


        src = imagem.get_attribute(
            "src"
        )

        alt = imagem.get_attribute(
            "alt"
        )


        navegador.close()


        return {
            "imagem": src,
            "descricao": alt
        }



def enviar_discord(tirinha):

    dados = {
        "embeds": [
            {
                "title": "Peanuts - Tirinha do dia",
                "description": tirinha["descricao"],
                "image": {
                    "url": tirinha["imagem"]
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
        print(resposta.text)



tirinha = pegar_tirinha()


if tirinha["imagem"]:

    print("Imagem encontrada:")
    print(tirinha["imagem"])

    enviar_discord(tirinha)

else:

    print("Não encontrei a tirinha")
