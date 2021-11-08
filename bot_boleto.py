from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class BotBoleto:
    
    def __init__(self, aluno, senha):
        self.aluno = aluno
        self.senha =  senha
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
    

    def login(self):
        driver = self.driver
        driver.get('https://novoportal.cruzeirodosul.edu.br/')
        sleep(3)
        campo_aluno = driver.find_element_by_xpath('//input[@name="username"]')
        campo_aluno.click()
        campo_aluno.clear()
        campo_aluno.send_keys(self.aluno)
        campo_senha = driver.find_element_by_xpath('//input[@name="password"]')
        campo_senha.click()
        campo_senha.clear()
        campo_senha.send_keys(self.senha)
        botao_area_aluno = driver.find_element_by_xpath('//button[contains(text(), "ÁREA DO ALUNO")]')
        botao_area_aluno.click()
        sleep(5)
        self.fechar_aba()
        self.financeiro()
    

    def fechar_aba(self):
        driver = self.driver
        fechar_aba1 = driver.find_element_by_xpath('html/body/app-root/app-template/div/app-modal-edit/div/div/div/div/button').click()
        sleep(3)
        try:
            fechar_aba2 = driver.find_element_by_xpath('html/body/app-root/app-template/div/app-documento-pendente-popup/app-modal/div/div/div/div/button').click()
        except:
            return


    def financeiro(self):
        driver = self.driver
        botao_financeiro = driver.find_element_by_xpath('//h4[contains(text(), "Financeiro")]')
        botao_financeiro.click()
        driver.get('https://novoportal.cruzeirodosul.edu.br/home/7/meus-pagamentos-novo')
        sleep(5)
        try:
            self.fechar_aba()
        except:
            sleep(2)
        sleep(2)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(1)
        boleto = driver.find_element_by_xpath('//button[@class="btn btn-sm btn-fazer-acordo"]')
        boleto.click()
        sleep(7)
        gerar_boleto = driver.find_element_by_xpath('//button[@class="btn btn-sm btn-pagar pagar-boleto"]')
        gerar_boleto.click()
        sleep(5)
        download_boleto = driver.find_element_by_xpath('//button[@class="btn btn-primary"]')
        download_boleto.click()
        sleep(4)
        driver.close()
        sleep(7)
        self.enviar_boleto_email('pablolanza75@gmail.com', 'cruzeiro')

    
    def enviar_boleto_email(self, email, senha):
        host = "smtp.gmail.com"
        port = "587"

        server = smtplib.SMTP(host, port)

        server.ehlo()
        server.starttls()
        server.login(email, senha)

        corpo = "Boleto"
        msg = MIMEMultipart()
        msg['Subject'] = 'Boleto Faculdade'
        msg['From'] = email
        msg['To'] = 'ana.lanza@hotmail.com'
        msg.attach(MIMEText(corpo, 'plain'))
        
        caminho_arquivo = 'C:\\Users\\Ana Paula\\Downloads\\boleto.pdf'
        attachment = open(caminho_arquivo, 'rb')
        att = MIMEBase('application', 'octet-stream')
        att.set_payload(attachment.read())
        encoders.encode_base64(att)

        att.add_header('Content-Disposition', 'attachment; filename=boleto.pdf')
        attachment.close()
        msg.attach(att)

        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        
     
    