from playwright.sync_api import sync_playwright
import requests
import os


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://www.gocomics.com/peanuts"


def pegar_tirinha():

    print("Iniciando Playwright...")

    with sync_playwright() as p:

        navegador = p.chromium.launch(
            headless=True
        )

        print("Navegador aberto")

        pagina = navegador.new_page()


        print("Abrindo GoComics...")

        pagina.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("Página carregada")

        pagina.wait_for_timeout(5000)

        print("Esperou JavaScript")


        quantidade = pagina.locator("img").count()

        print(
            "Quantidade de imagens:",
            quantidade
        )


        quantidade_comic = pagina.locator(
            "img[class*='comic__image']"
        ).count()

        print(
            "Quantidade de comic__image:",
            quantidade_comic
        )


        if quantidade_comic == 0:

            print(
                "Nenhuma tirinha encontrada"
            )

            navegador.close()

            return None


        comic = pagina.locator(
            "img[class*='comic__image']"
        ).first


        imagem = comic.get_attribute(
            "src"
        )

        descricao = comic.get_attribute(
            "alt"
        )


        print(
            "Imagem encontrada:",
            imagem
        )

        print(
            "Descrição:",
            descricao
        )


        navegador.close()


        return {
            "imagem": imagem,
            "descricao": descricao
        }



def enviar_discord(tirinha):

    print("Enviando para Discord...")


    resposta = requests.post(
        WEBHOOK,
        json={
            "username": "Daily Comics",
            "embeds": [
                {
                    "title": "Peanuts - Tirinha do dia",
                    "description": tirinha["descricao"],
                    "image": {
                        "url": tirinha["imagem"]
                    }
                }
            ]
        }
    )


    print(
        "Resposta Discord:",
        resposta.status_code
    )



tirinha = pegar_tirinha()


if tirinha:

    enviar_discord(tirinha)

else:

    print(
        "Processo finalizado sem tirinha"
    )
