from playwright.sync_api import sync_playwright


URL = "https://www.gocomics.com/peanuts"


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


    # Dá tempo para o JavaScript carregar
    pagina.wait_for_timeout(5000)


    print("Título da página:")
    print(
        pagina.title()
    )


    print("\nURL atual:")
    print(
        pagina.url
    )


    print("\nTexto encontrado na página:")
    texto = pagina.locator(
        "body"
    ).inner_text()

    print(
        texto[:2000]
    )


    # Conta elementos importantes
    print("\nQuantidade de imagens:")
    print(
        pagina.locator("img").count()
    )


    print("\nQuantidade de elementos:")
    print(
        pagina.locator("*").count()
    )


    # Salva uma captura para análise
    pagina.screenshot(
        path="debug.png",
        full_page=True
    )


    navegador.close()
