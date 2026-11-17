import rpa as R
import pyautogui as P
import pandas as PD

R.init()
R.url('http://rpachallenge.com')
janela = P.getActiveWindow()
janela.maximize()
P.sleep(7)

R.download('http://rpachallenge.com/assets/downloadFiles/challenge.xlsx', 'challenge.xlsx')
P.sleep(1)

dados = PD.read_excel('challenge.xlsx', sheet_name='Sheet1')

df = PD.DataFrame(dados, columns=["First Name",	"Last Name ", "Company Name", "Role in Company", "Address", "Email", "Phone Number"])

R.click('/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button')

for row in df.itertuples():
    R.type('//*[@ng-reflect-name="labelFirstName"]', row[1])
    R.type('//*[@ng-reflect-name="labelLastName"]', row[2])
    R.type('//*[@ng-reflect-name="labelCompanyName"]', row[3])
    R.type('//*[@ng-reflect-name="labelRole"]', row[4])
    R.type('//*[@ng-reflect-name="labelAddress"]', row[5])
    R.type('//*[@ng-reflect-name="labelEmail"]', row[6])
    R.type('//*[@ng-reflect-name="labelPhone"]', str(row[7]))
    R.click('/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/input')
P.sleep(5)
P.screenshot('score_do_site_rpachallenge.png')
P.close()