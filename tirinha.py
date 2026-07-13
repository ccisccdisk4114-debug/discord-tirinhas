from playwright.sync_api import sync_playwright
import requests
import os
from datetime import datetime


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
            wait_until="domcontentloaded",
            timeout=60000
        )


        # Aguarda um pouco para o JavaScript terminar
        pagina.wait_for_timeout(5000)


        imagens = pagina.locator("img")

        quantidade = imagens.count()


        print("Quantidade de imagens encontradas:", quantidade)


        tirinha = None


        for i in range(quantidade):

            imagem = imagens.nth(i)

            alt = imagem.get_attribute("alt")
            src = imagem.get_attribute("src")


            print("\nImagem", i)
            print("ALT:", alt)
            print("SRC:", src)


            # Procura o padrão da tirinha do GoComics
            if (
                alt
                and "undefined for" in alt
                and src
            ):
                tirinha = {
                    "imagem": src,
                    "descricao": alt
                }

                break


        navegador.close()


        return tirinha



def enviar_discord(tirinha):

    data = datetime.now().strftime(
        "%d/%m/%Y"
    )


    dados = {

        "username": "Daily Comics",

        "embeds": [

            {

                "title": "Peanuts - Tirinha do dia",

                "description": (
                    f"{tirinha['descricao']}\n\n"
                    f"Data: {data}"
                ),

                "image": {

                    "url": tirinha["imagem"]

                },

                "footer": {

                    "text": "Postado automaticamente"

                }

            }

        ]

    }


    resposta = requests.post(
        WEBHOOK,
        json=dados
    )


    if resposta.status_code != 204:

        print(
            "Erro ao enviar Discord:"
        )

        print(
            resposta.text
        )




tirinha = pegar_tirinha()


if tirinha:

    print("\nTirinha encontrada:")
    print(tirinha)


    enviar_discord(tirinha)


else:

    print(
        "\nNão foi possível encontrar a tirinha."
    )
