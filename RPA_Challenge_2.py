import rpa as R
import pyautogui as P
import pandas as PD
import os as O

R.init()
R.url('https://rpachallengeocr.azurewebsites.net/')
janela = P.getActiveWindow()
janela.maximize()
P.sleep(7)

countPage = 1
while countPage <= 3:
    if countPage == 1:
        R.table('//*[@id="tableSandbox"]', 'Temp.csv')
        dados = PD.read_csv('Temp.csv')
        dados.to_csv(r'WebTable.csv', mode='a', index=None, header=True)
        R.click('//*[@id="tableSandbox_next"]')
        countPage = countPage + 1
    else:
        R.table('//*[@id="tableSandbox"]', 'Temp.csv')
        dados = PD.read_csv('Temp.csv')
        dados.to_csv(r'WebTable.csv', mode='a', index=None, header=False)
        R.click('//*[@id="tableSandbox_next"]')
        countPage = countPage + 1
R.close()
O.remove('Temp.csv')
csv_xlsx = PD.read_csv(r'WebTable.csv')
csv_xlsx.to_excel(r'WebTable02.xlsx')


