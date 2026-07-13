from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
import os
from datetime import datetime


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://www.gocomics.com/peanuts"



def abrir_pagina():

    with sync_playwright() as p:

        navegador = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )


        contexto = navegador.new_context(

            viewport={
                "width": 1280,
                "height": 900
            },

            locale="en-US",

            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )

        )


        pagina = contexto.new_page()


        print("Abrindo GoComics...")


        pagina.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000
        )


        print("Página carregada")


        try:

            pagina.wait_for_selector(
                "img[class*='comic__image'][alt*='for']",
                timeout=60000
            )


        except PlaywrightTimeoutError:


            print(
                "A tirinha não apareceu no tempo esperado"
            )


            pagina.screenshot(
                path="debug.png",
                full_page=True
            )


            with open(
                "pagina_debug.html",
                "w",
                encoding="utf-8"
            ) as arquivo:

                arquivo.write(
                    pagina.content()
                )


            navegador.close()


            return None



        comic = pagina.locator(
            "img[class*='comic__image'][alt*='for']"
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
            "Descrição original:",
            descricao
        )


        navegador.close()



        return {

            "imagem": imagem,

            "descricao": descricao

        }




def pegar_tirinha():

    tentativas = 3


    for tentativa in range(1, tentativas + 1):


        print(
            f"Tentativa {tentativa}/{tentativas}"
        )


        resultado = abrir_pagina()


        if resultado:

            return resultado



        print(
            "Falhou, tentando novamente..."
        )



    return None




def formatar_descricao(tirinha):


    data = datetime.now().strftime(
        "%d/%m/%Y"
    )


    return (
        f"🐱 **Peanuts Daily Comic**\n\n"
        f"📅 {data}\n\n"
        f"Charles Schulz"
    )





def enviar_discord(tirinha):


    print(
        "Enviando para Discord..."
    )


    dados = {


        "username": "Daily Comics",


        "embeds": [

            {

                "title": "Peanuts - Tirinha do dia",

                "description": formatar_descricao(
                    tirinha
                ),

                "image": {

                    "url": tirinha["imagem"]

                },

                "footer": {

                    "text": "Automated Daily Comics"

                }

            }

        ]

    }



    resposta = requests.post(
        WEBHOOK,
        json=dados
    )


    print(
        "Resposta Discord:",
        resposta.status_code
    )





tirinha = pegar_tirinha()



if tirinha:


    enviar_discord(
        tirinha
    )


else:


    print(
        "Não foi possível obter a tirinha"
    )
