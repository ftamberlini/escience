#Disciplina: E-science
#Script: capturaNAV.py
#Objetivo: Capturar as Tag (assunto) e Títulos dos vídeos do YouTube sem alterar configurações com histórico de navegação anterior

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
urlNav = 'http://www.google.com.br/search?q='
temasNav = ['campeonato brasileiro','viagem exterior','brinquedos infantil','filmes no cinema','musicas mais tocadas']
indNomeArq=['01','02','03','04','05']

option = Options()
option.headless = True

mAssunto=[]
mTitulo=[]
nmArqAssunto="dAssunto_C2_"
nmArqTitulo="dTitulo_C2_"

for  j,nav in enumerate(temasNav):
    for i in range(qtdIteracoes):
        #Executando em background
        driver = webdriver.Firefox(options=option)
        #driver = webdriver.Firefox()

        #Abrindo a URL do youtube
        driver.get(urlNav + nav)
        time.sleep(tEspera)

        driver.find_element_by_tag_name('h3').click()

        time.sleep(tEspera)

        #Tempo para carregar
        time.sleep(tEspera)

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



