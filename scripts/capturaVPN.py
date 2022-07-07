#Disciplina: E-science
#Script: capturaVPN.py
#Objetivo: Capturar as Tag (assunto) e Títulos dos vídeos do YouTube com alteração de configuração de idioma no Navegador e uso de VPN do local do idioma

from locale import windows_locale
import os, locale, ctypes

from re import M
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
from datetime import datetime

qtdIteracoes = 10
tEspera = 5
url = 'http://youtube.com'

idiomas = ['ja-JP, ja']
siglas = ['ja_JP.UTF-8']
indNomeArq=['01','02','03','04','05']

option = Options()
option.headless = True

mAssunto=[]
mTitulo=[]
nmArqAssunto="dAssunto_C3_"
nmArqTitulo="dTitulo_C3_"

for  j,nav in enumerate(idiomas):
    locale.setlocale(locale.LC_ALL,siglas[j])
    for i in range(qtdIteracoes):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('intl.accept_languages',idiomas[j])
        
        #Executando em background
        #driver = webdriver.Firefox(options=option)
        
        #Abrindo o navegador
        driver = webdriver.Firefox(firefox_profile=profile)
        
        #Abrindo a URL do youtube
        driver.get(url)

        #Tempo para carregar
        time.sleep(tEspera)
        
        #Capturando o Assunto pela iron-selecto TAG do youtube 
        dataAssunto = pd.Timestamp.now()
        eAssunto = driver.find_element_by_tag_name('iron-selector')
        htmlAssunto = eAssunto.get_attribute('outerHTML')
        soupAssunto = BeautifulSoup(htmlAssunto,'html.parser')

        #Salvando as n Tag(Assunto) num vetor para cada iteração para depois salvar o resultado total na matriz
        vAssunto=[]
        for assunto in soupAssunto.find_all('yt-formatted-string'):
            vAssunto.append(assunto.getText())
        mAssunto.append(vAssunto)
        #dfAssunto.insert(i,'Assunto'+str(i), vAssunto)	

        #Capturando os titulos pela id contents do youtube
        dataTitulo = pd.Timestamp.now()
        eTitulo = driver.find_element_by_id('contents')
        htmlTitulo = eTitulo.get_attribute('outerHTML')
        soupTitulo = BeautifulSoup(htmlTitulo,'html.parser')

        #Salvando os titulos num vetor para cada iteração para depois salvar o resultado total na matriz
        vTitulo=[]
        for titulo in soupTitulo.find_all('yt-formatted-string'):
            vTitulo.append(titulo.getText())
        mTitulo.append(vTitulo)
        #dfTitulo.insert(i,'Titulo'+str(i), vTitulo)	

        driver.quit()

    dfAssunto = pd.DataFrame(mAssunto)
    dfTitulo = pd.DataFrame(mTitulo)

    nmDH = str(datetime.now().strftime("%Y%m%d_%H%M%S"))
   
    nmArq=nmArqAssunto+indNomeArq[j]+'_'+nmDH+'.csv'
    dfAssunto.to_csv(nmArq,sep=';',encoding="utf-8") 
   
    nmArq=nmArqAssunto+'ALL.csv'
    dfAssunto.to_csv(nmArq,sep=';',encoding="utf-8",mode="a",header=False)
   
    nmArq=nmArqTitulo+indNomeArq[j]+'_'+nmDH+'.csv'
    dfTitulo.to_csv(nmArq,sep=';',encoding="utf-8")
   
    nmArq=nmArqTitulo+'ALL.csv'
    dfTitulo.to_csv(nmArq,sep=';',encoding="utf-8",mode="a",header=False)
    
    mAssunto.clear()
    mTitulo.clear()
