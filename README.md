# 🤖 RPA Challenges

Automações em Python para dois desafios públicos de RPA, cada um implementado em **duas versões**: uma com a biblioteca `rpa` (TagUI) + PyAutoGUI e outra com o framework **BotCity**.

## 📁 Estrutura do repositório

```
.
├── RPA_Challenge.py                    # Desafio 1 – versão rpa (TagUI) + PyAutoGUI
├── RPA_Challenge_1_versao_botcity.py   # Desafio 1 – versão BotCity
├── RPA_Challenge_2.py                  # Desafio 2 – versão rpa (TagUI) + PyAutoGUI
└── RPA_Challenge_2_versao_botcity.py   # Desafio 2 – versão BotCity
```

## 🎯 Os desafios

### Desafio 1 – Preenchimento de formulários
**Site:** https://rpachallenge.com/

O site apresenta um formulário cujos campos mudam de posição a cada rodada. A automação deve:

1. Baixar a planilha `challenge.xlsx` com 10 registros;
2. Clicar em **Start** para iniciar o cronômetro;
3. Preencher os 7 campos (First Name, Last Name, Company Name, Role in Company, Address, Email, Phone Number) e clicar em **Submit**, 10 vezes;
4. Capturar a tela com a pontuação final (`score_do_site_rpachallenge.png`).

Como os campos são embaralhados, os scripts localizam cada um pelo atributo `ng-reflect-name` (ex.: `labelFirstName`), e não pela posição.

### Desafio 2 – Extração de tabela web
**Site:** https://rpachallengeocr.azurewebsites.net/

A automação deve extrair os dados da tabela `#tableSandbox`, percorrendo as **3 primeiras páginas** (botão *Next*), e consolidar tudo em um arquivo Excel (`WebTable02.xlsx`).

## 🔀 Comparativo das versões

| Aspecto | Versão `rpa` + PyAutoGUI | Versão BotCity |
|---|---|---|
| Biblioteca principal | `rpa` (TagUI), `pyautogui` | `botcity-web-plugin` |
| Download do Excel (Desafio 1) | `R.download(...)` | `requests.get(...)` |
| Maximizar janela | `pyautogui.getActiveWindow().maximize()` | `bot.maximize_window()` |
| Espera de carregamento | `P.sleep(7)` fixo | `waiting_time` nos elementos + `bot.wait()` |
| Extração da tabela (Desafio 2) | `R.table()` → CSV temporário → CSV final → Excel | `table_to_dict()` → DataFrame → Excel |
| Arquivos intermediários | `Temp.csv`, `WebTable.csv` | Nenhum |
| Tratamento de erros | Não possui | `try/except/finally` |
| Driver do Chrome | Gerenciado pelo TagUI | `webdriver-manager` (automático) |
| Integração com orquestrador | Não | BotCity Maestro (opcional) |

## ⚙️ Pré-requisitos

- Python 3.9+
- Google Chrome instalado
- Conexão com a internet

## 📦 Instalação

### Versões `rpa` + PyAutoGUI

```bash
pip install rpa pyautogui pandas openpyxl
```

### Versões BotCity

```bash
pip install botcity-web-plugin botcity-maestro-sdk pandas openpyxl requests webdriver-manager
```

> `openpyxl` é necessário para o pandas ler e escrever arquivos `.xlsx`.

## ▶️ Como executar

```bash
# Desafio 1
python RPA_Challenge.py
python RPA_Challenge_1_versao_botcity.py

# Desafio 2
python RPA_Challenge_2.py
python RPA_Challenge_2_versao_botcity.py
```

Os scripts BotCity também podem ser executados via **BotCity Maestro**. Sem conexão com o orquestrador, o `BotMaestroSDK.RAISE_NOT_CONNECTED = False` evita erros e o script roda normalmente de forma local.

## 📤 Arquivos gerados

| Arquivo | Gerado por | Descrição |
|---|---|---|
| `challenge.xlsx` | Desafio 1 | Planilha de entrada baixada do site |
| `score_do_site_rpachallenge.png` | Desafio 1 | Print da pontuação final |
| `WebTable.csv` | Desafio 2 (`rpa`) | Dados consolidados em CSV |
| `WebTable02.xlsx` | Desafio 2 (ambas) | Tabela final extraída, em Excel |

## 🛠️ Ajustes e melhorias sugeridas

- **`RPA_Challenge.py`:** a última linha usa `P.close()`, mas o PyAutoGUI não possui esse método. O correto seria `R.close()` para encerrar o navegador do `rpa`.
- **`RPA_Challenge.py`:** o nome da coluna `"Last Name "` está com espaço no final, porque a planilha original vem assim. A versão BotCity já trata isso com `dados.columns.str.strip()`.
- **`RPA_Challenge_2.py`:** o `WebTable.csv` é aberto em modo `append`; rodar o script mais de uma vez duplica os dados. Apagar o arquivo antes de iniciar resolve.
- **`RPA_Challenge_2.py`:** `to_excel` sem `index=False` grava uma coluna extra de índice no Excel.
- **Esperas fixas:** `P.sleep()` e `bot.wait()` podem ser trocados por esperas por elemento para maior estabilidade.
- **Maestro:** descomentar a linha `maestro.error(...)` no `except` para registrar falhas no orquestrador.

## 📚 Referências

- [RPA Challenge](https://rpachallenge.com/)
- [RPA Challenge OCR](https://rpachallengeocr.azurewebsites.net/)
- [Documentação BotCity](https://documentation.botcity.dev/)
- [rpa-python (TagUI)](https://github.com/tebelorg/RPA-Python)
