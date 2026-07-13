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


        # Espera o JavaScript carregar a tirinha
        pagina.wait_for_timeout(5000)


        pagina.wait_for_selector(
            "img[class*='comic__image']",
            timeout=60000
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


        navegador.close()


        return {
            "imagem": imagem,
            "descricao": descricao
        }
