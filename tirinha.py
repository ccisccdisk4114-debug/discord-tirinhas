from playwright.sync_api import sync_playwright
import requests
import os


WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://www.gocomics.com/peanuts"



def pegar_tirinha():

    print("Iniciando Playwright...")

    with sync_playwright() as p:

        navegador = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        print("Navegador aberto")


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


        # Tempo para a verificação automática e JavaScript
        pagina.wait_for_timeout(15000)


        print("Esperou carregamento")


        print(
            "Título:",
            pagina.title()
        )


        print(
            "URL:",
            pagina.url
        )


        quantidade_imagens = pagina.locator(
            "img"
        ).count()


        print(
            "Quantidade de imagens:",
            quantidade_imagens
        )


        quantidade_comic = pagina.locator(
            "img[class*='comic__image']"
        ).count()


        print(
            "Quantidade de comic__image:",
            quantidade_comic
        )


        # Diagnóstico caso ainda esteja na tela de segurança
        if quantidade_comic == 0:


            print(
                "Nenhuma tirinha encontrada"
            )


            conteudo = pagina.content()


            with open(
                "pagina_debug.html",
                "w",
                encoding="utf-8"
            ) as arquivo:

                arquivo.write(
                    conteudo
                )


            print(
                "HTML salvo"
            )


            pagina.screenshot(
                path="debug.png",
                full_page=True
            )


            print(
                "Screenshot salvo"
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


    print(
        "Enviando para Discord..."
    )


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

    enviar_discord(
        tirinha
    )


else:

    print(
        "Processo finalizado sem tirinha"
    )
