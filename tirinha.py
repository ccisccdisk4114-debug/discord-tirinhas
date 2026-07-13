from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
import os
import random
from datetime import datetime


WEBHOOK = os.environ["DISCORD_WEBHOOK"]


COMICS = {

    "Peanuts": "https://www.gocomics.com/peanuts",

    "Garfield": "https://www.gocomics.com/garfield",

    "Calvin and Hobbes": "https://www.gocomics.com/calvinandhobbes"

}



def escolher_tirinha():

    nome, url = random.choice(
        list(COMICS.items())
    )

    print(
        f"Tirinha escolhida: {nome}"
    )

    return nome, url





def abrir_pagina(nome, url):

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



        print(
            f"Abrindo {nome}..."
        )



        pagina.goto(

            url,

            wait_until="domcontentloaded",

            timeout=60000

        )



        print(
            "Página carregada"
        )



        try:


            pagina.wait_for_selector(

                "img[class*='comic__image']",

                timeout=60000

            )


        except PlaywrightTimeoutError:


            print(
                "A tirinha não apareceu"
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




        quantidade = pagina.locator(

            "img[class*='comic__image']"

        ).count()



        print(

            "Quantidade de tirinhas encontradas:",

            quantidade

        )



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


            "nome": nome,


            "imagem": imagem,


            "descricao": descricao


        }





def pegar_tirinha():


    for tentativa in range(1, 4):


        print(

            f"Tentativa {tentativa}/3"

        )



        nome, url = escolher_tirinha()



        resultado = abrir_pagina(

            nome,

            url

        )



        if resultado:


            return resultado



        print(

            "Falhou, tentando novamente..."

        )



    return None





def enviar_discord(tirinha):


    print(

        "Enviando para Discord..."

    )



    data = datetime.now().strftime(

        "%d/%m/%Y"

    )



    dados = {


        "username": "Daily Comics",



        "embeds": [


            {


                "title":

                f"{tirinha['nome']} - Tirinha do dia",



                "description":

                (

                    f"📅 {data}\n\n"

                    "Automated Daily Comics"

                ),



                "image": {


                    "url":

                    tirinha["imagem"]


                },



                "footer": {


                    "text":

                    "GoComics"

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

        "Não foi possível obter nenhuma tirinha"

    )
