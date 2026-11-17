import os
import requests
import pandas as pd
from botcity.web import WebBot, Browser, By
from webdriver_manager.chrome import ChromeDriverManager

# Importações padrão do BotCity Maestro (Opcional)
from botcity.maestro import *
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()

    arquivo_excel = "challenge.xlsx"

    try:
        # 1. Faz o download direto do arquivo Excel (mais rápido e confiável que clicar no botão)
        url_excel = "https://rpachallenge.com/assets/downloadFiles/challenge.xlsx"
        resposta = requests.get(url_excel)
        with open(arquivo_excel, "wb") as f:
            f.write(resposta.content)

        # 2. Lê a planilha com Pandas (limpando espaços extras nos nomes das colunas por segurança)
        dados = pd.read_excel(arquivo_excel, sheet_name="Sheet1")
        dados.columns = dados.columns.str.strip()

        colunas = [
            "First Name",
            "Last Name",
            "Company Name",
            "Role in Company",
            "Address",
            "Email",
            "Phone Number",
        ]
        df = dados[colunas]

        # 3. Abre o site e maximiza a janela
        bot.browse("https://rpachallenge.com/")
        bot.maximize_window()

        # Aguarda o botão "Start" carregar e clica nele para iniciar o cronômetro
        botao_start = bot.find_element("//button[text()='Start']", By.XPATH, waiting_time=10000)
        botao_start.click()

        # 4. Preenche os 10 formulários dinâmicos
        for row in df.itertuples(index=False):
            bot.find_element('//*[@ng-reflect-name="labelFirstName"]', By.XPATH).send_keys(str(row[0]))
            bot.find_element('//*[@ng-reflect-name="labelLastName"]', By.XPATH).send_keys(str(row[1]))
            bot.find_element('//*[@ng-reflect-name="labelCompanyName"]', By.XPATH).send_keys(str(row[2]))
            bot.find_element('//*[@ng-reflect-name="labelRole"]', By.XPATH).send_keys(str(row[3]))
            bot.find_element('//*[@ng-reflect-name="labelAddress"]', By.XPATH).send_keys(str(row[4]))
            bot.find_element('//*[@ng-reflect-name="labelEmail"]', By.XPATH).send_keys(str(row[5]))
            bot.find_element('//*[@ng-reflect-name="labelPhone"]', By.XPATH).send_keys(str(row[6]))

            # Clica em Submit
            bot.find_element('//input[@type="submit"]', By.XPATH).click()

        # 5. Aguarda a tela de pontuação aparecer e tira o print nativamente pelo navegador
        bot.wait(2000)
        bot.save_screenshot("score_do_site_rpachallenge.png")
        print("Desafio concluído! Screenshot salvo em 'score_do_site_rpachallenge.png'.")

    except Exception as ex:
        print(f"Erro durante a execução: {ex}")

    finally:
        bot.wait(2000)
        bot.stop_browser()


if __name__ == "__main__":
    main()