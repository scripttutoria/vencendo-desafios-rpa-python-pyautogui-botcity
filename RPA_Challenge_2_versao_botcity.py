import pandas as pd
from botcity.web import WebBot, Browser, By
from botcity.web.util import element_as_select
from botcity.web.parsers import table_to_dict
from webdriver_manager.chrome import ChromeDriverManager

# Importações para integração com o BotCity Maestro (Opcional, padrão do template)
from botcity.maestro import *
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Inicialização do Maestro (caso rode via Orquestrador)
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    # Instancia o WebBot
    bot = WebBot()

    # Define se rodará em segundo plano (False = abre o navegador visualmente)
    bot.headless = False

    # Configura o navegador (Chrome) e baixa o driver compatível automaticamente
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()

    try:
        # Acessa a URL e maximiza a janela nativamente
        bot.browse("https://rpachallengeocr.azurewebsites.net/")
        bot.maximize_window()

        # Aguarda a tabela carregar na página (até 10 segundos)
        tabela_elemento = bot.find_element('//*[@id="tableSandbox"]', By.XPATH, waiting_time=10000)

        lista_dados = []
        count_page = 1

        while count_page <= 3:
            # Localiza a tabela atualizada na página
            tabela_elemento = bot.find_element('//*[@id="tableSandbox"]', By.XPATH)

            # Extrai os dados da tabela diretamente para uma lista de dicionários
            dados_pagina = table_to_dict(table=tabela_elemento)
            lista_dados.extend(dados_pagina)

            # Clica no botão "Next" se ainda não estiver na última página desejada
            if count_page < 3:
                botao_next = bot.find_element('//*[@id="tableSandbox_next"]', By.XPATH)
                botao_next.click()
                bot.wait(1000)  # Pequena pausa (1s) para atualização do DOM

            count_page += 1

        # Converte todos os dados acumulados em um único DataFrame e salva em Excel
        df_final = pd.DataFrame(lista_dados)
        df_final.to_excel("WebTable02.xlsx", index=False)

        print("Extração concluída com sucesso! Arquivo 'WebTable02.xlsx' gerado.")

    except Exception as ex:
        print(f"Erro durante a execução: {ex}")
        # Caso use o Maestro, registra o erro:
        # maestro.error(task_id=execution.task_id, exception=ex)

    finally:
        # Encerra o navegador e libera recursos
        bot.wait(2000)
        bot.stop_browser()


if __name__ == "__main__":
    main()