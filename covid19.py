#!/usr/bin/env python3

#
#--------------------------------------------------------------------------------
#--                                                                            --
#--                 Universidade Federal de Santa Maria                        --
#--                        Centro de Tecnologia                                --
#--                 Curso de Engenharia de Computação                          --
#--                 Santa Maria - Rio Grande do Sul/BR                         --
#--                                                                            --
#--------------------------------------------------------------------------------
#--                                                                            --
#-- Design      :                                                              --
#-- File		: covid19                  	                              	   --
#-- Authors     : Luis Felipe de Deus                                          --
# --Mentors     :                                                              -- 
#--                                                                            -- 
#--------------------------------------------------------------------------------
#--                                                                            --
#-- Created     : 02 Apr 2020                                                  --
#-- Update      : 02 Apr 2020                                                  --
#--------------------------------------------------------------------------------
#--                              Overview                                      --
#--                                                                            --
#-- Code executed in python3                                                   --
#--------------------------------------------------------------------------------
#

#Import the libraries which we need
import COVID19Py
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import io
import sys
import requests
from copy import copy

# @brief: Make some linear graphics
# @param: c1, c2, c3, c4 are the countries objects
# @return: void
def doGraphics(c1, c2, c3, c4):
    #Todos tem mesmo tamanho em dias
    x = np.linspace(0, len(c1.getData()), len(c1.getData()), endpoint=True)
    #-1 acessa ultima linha (dia mais recente) e o 1 acessa posição de casos acumulados
    y_br = [v for k,v,f in c1.getData()]     
    y_usa = [v for k,v,f in c2.getData()]   
    y_it = [v for k,v,f in c3.getData()]   
    y_es = [v for k,v,f in c4.getData()]   
 
    plt.figure('Covid-19 confirmed case curve', figsize=(14,6))

    plt.subplot(2,2,1)
    plt.title("Brazil")
    plt.ylabel("Number of cases")
    plt.xlabel("Days")
    plt.plot(x, y_br, "blue")
    plt.grid()

    plt.subplot(2,2,2)
    plt.title("USA")
    plt.ylabel("Number of cases")
    plt.xlabel("Days")
    plt.plot(x, y_usa, "black")
    plt.grid()

    plt.subplot(2,2,3)
    plt.title("Italy")
    plt.ylabel("Number of cases")
    plt.xlabel("Days")
    plt.plot(x, y_it, "blue")
    plt.grid()

    plt.subplot(2,2,4)
    plt.title("Spain")
    plt.ylabel("Number of cases")
    plt.xlabel("Days")
    plt.plot(x, y_es, "black")
    plt.grid()
        
    plt.show()
#end

# @brief: Make some bar graphics
# @param: c1, c2, c3, c4 are the countries objects
# @return: void
def doBarGraph(c1, c2, c3, c4):
    bar_width = 0.25
    timeline = [k for k,v,f in c1.getData()]
    r1 = np.arange(len(timeline))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    r4 = [x + bar_width for x in r3]

    plt.figure('Covid-19 confirmed case curve', figsize=(14,6))
    #Grafico em barra do crescimento dos 4 paises
    plt.subplot(2,2,1)    
    plt.bar(r1, [v for k,v,f in c1.getData()]  , color = c1.country_color, label = c1.country_name)
    plt.bar(r2, [v for k,v,f in c2.getData()]  , color = c2.country_color, label = c2.country_name)
    plt.bar(r3, [v for k,v,f in c3.getData()]  , color = c3.country_color, label = c3.country_name)
    plt.bar(r4, [v for k,v,f in c4.getData()]  , color = c4.country_color, label = c4.country_name)
    plt.xticks([r + bar_width for r in range(len(timeline))], timeline, rotation = 90)
    plt.ylabel("Number of cases", fontsize = 'large',fontweight = 'bold')
    plt.xlabel("Timeline", fontsize = 'large',fontweight = 'bold')
    plt.legend(fontsize = 'large')
    #plt.grid()
    

    #Grafico em barra do crescimento USA x Espanha
    plt.subplot(2,2,2)
    plt.bar(r1, [v for k,v,f in c2.getData()], color = c2.country_color, label = c2.country_name)
    plt.bar(r2, [v for k,v,f in c4.getData()], color = c4.country_color, label = c3.country_name)
    plt.xticks([r + bar_width for r in range(len(timeline))], timeline, rotation = 90)
    plt.ylabel("Number of cases", fontsize = 'large',fontweight = 'bold')
    plt.xlabel("Timeline", fontsize = 'large',fontweight = 'bold')
    plt.legend(fontsize = 'large')
    #plt.grid()

    #Grafico em barra do crescimento Italia x Brasil
    plt.subplot(2,2,3)
    plt.bar(r1, [v for k,v,f in c3.getData()], color = c3.country_color, label = c3.country_name)
    plt.bar(r2, [v for k,v,f in c1.getData()], color = c1.country_color, label = c1.country_name)
    plt.xticks([r + bar_width for r in range(len(timeline))], timeline, rotation = 90)
    plt.ylabel("Number of cases", fontsize = 'large',fontweight = 'bold')
    plt.xlabel("Timeline", fontsize = 'large',fontweight = 'bold')
    plt.legend(fontsize = 'large')
    #plt.grid()

    plt.subplot(2,2,4)
    plt.barh(c1.country_name, c1.getData()[-1][1], color = c1.country_color)
    plt.barh(c2.country_name, c2.getData()[-1][1], color = c2.country_color)
    plt.barh(c3.country_name, c3.getData()[-1][1], color = c3.country_color)
    plt.barh(c4.country_name, c4.getData()[-1][1], color = c4.country_color)
    #plt.title("Comparing number of cases per countries", fontsize = 'large',fontweight = 'bold' )
    plt.xlabel("Number of cases", fontsize = 'large',fontweight = 'bold')
    plt.ylabel("Countries", fontsize = 'large',fontweight = 'bold')
    #plt.grid()
    plt.show()

# @brief: Make a linear regression bases on cases/day and days (NOT ready yet!!!)
# @param: country is the object from some country
# @param: label is the type of data which one you want use like newCases, Cases or deaths
# @return: void
class linearRegressionModel():
    def __init__(self, country, label):
        self.country = country
        self.acquisitionName = label 
        self.model = LinearRegression()
    def computeModel(self, prediction = [80,81,82,83]):
        #Cria um array baseado na label informada
        if(self.acquisitionName == 'newCases'): self.dataYf = np.array([f for k,v,f in self.country.getData()])
        elif(self.acquisitionName == 'Cases'): self.dataYf = np.array([v for k,v,f in self.country.getData()])
        elif(self.acquisitionName == 'Deaths'): self.dataYf = np.array([v for k,v,f in self.country.getData()])
        #Cria um array de dias absolutos
        self.dataXf = np.array(range(len(self.country.getData()))).reshape((-1, 1))
        
        #Refatora o array para pegar so a partir da inclinação da curva
        self.dataY = self.dataYf[60:]
        self.dataX = self.dataXf[60:]

        #treina o modelo
        self.model.fit(self.dataX, self.dataY)
        #Cria um array de teste
        newX = np.array(prediction).reshape((-1, 1))
        #Aplica os novos dias ao modelo e estima o Y
        self.yPred = self.model.predict(newX)
        print("\n---- Prediction ------")
        for i, y in enumerate(self.yPred):
            print("X: ", newX[i], "Y: %.2f"%(y))
    
    def getModel(self):
        return self.model
    
    def getPredicition(self):
        return self.yPred

    def doGraphic(self):
        #Plota Gaficos de regressão
        plt.figure('Covid-19 ', figsize=(14,6))
        #Grafico em barra do crescimento dos 4 paises
        plt.subplot(1,2,1)    
        plt.scatter(self.dataX, self.dataY)
        plt.plot(self.dataX, self.model.predict(self.dataX), color = 'red' )
        plt.title("Linear Regression for %s"%(self.acquisitionName), fontsize = 'large',fontweight = 'bold')
        plt.ylabel("Cases", fontsize = 'large',fontweight = 'bold')
        plt.xlabel("Absolute days", fontsize = 'large',fontweight = 'bold')

        plt.subplot(1,2,2)    
        plt.plot(self.dataXf, self.dataYf)
        plt.title("Linear Distribution", fontsize = 'large',fontweight = 'bold')
        plt.ylabel("Cases", fontsize = 'large',fontweight = 'bold')
        plt.xlabel("Absolute days", fontsize = 'large',fontweight = 'bold')

        plt.show()



class WorldAgainstCovid19():
    def __init__(self, countries):
        self.countriesNames = countries
        self.countries = []
        for country in self.countriesNames:
            self.c = CountryAgainstCovid19(name=country, code=country)
            self.c.setData_URL()

            #Verifica se tem mais de uma ocorrencia do pais caso tenha mais de uma data igual
            cont = 0
            for x,y,z in self.c.getData():
                if(x =='1-22'): cont+=1
            #Se existe, da um merge nos dados somando os casos
            if (cont>1): 
                self.mergeSameCountry(country, country, cont)
           
            self.countries.append(self.c)

    def mergeSameCountry(self, country, code, cont):
        print(" -- Merge Country in %d:1 parts--"%(cont))
        #Cria um objeto copia
        cCopy = CountryAgainstCovid19(name=country, code=code)
        cCopy.setData_URL()

        #Reeseta os dados do original
        self.c.resetData()
        #Cria uma variavel step que é o passo de ocorrencia de cada data
        step = int((len(cCopy.getData())/cont))
        #Cria um laço de 0 até numero de ocorrencias 
        for i in range(step):
            acc1,acc2 = 0,0
            #Cria um laço para pegar sempre todos os valores de uma data e acumular
            for x,y,z in cCopy.getData()[i::step]:
                acc1+=y
                acc2+=z
            #Uma vez todos os valores de um dia acumulados, adiciona no objeto original
            self.c.DailyCases.append([x,int(acc1),int(acc2)])

    def getCountries(self):
        return self.countries

    def doGraphic(self, data):
        fig1, ax1 = plt.subplots()
        ax1.pie(data, labels = self.countriesNames, autopct = '%1.1f%%', shadow = True, startangle=90)
        ax1.axis('equal')
        plt.show()

# @brief: Object from country, we have a setData function which one receive dada from API and set into the class and getData return this data as a list
# @param: covid19 is the API object
# @param: name is the country name such as Brazil
# @param: code is the country code such as BR, US, IT
# @param: color is a arbitrary color for the graphics
class CountryAgainstCovid19():
    def __init__(self, covid19=0, name='', code='', color='purple'):
        self.country_name = name
        self.country_code = code
        self.country_color = color
        self.covid19 = covid19
        self.DailyCases = []
        
    def setData_URL(self, url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'):
        try:
            rawData=requests.get(url).text.encode()
        except:
            print("Erro de conexão aos Dados...")
            print("FInalizando programa")
            sys.exit()

        rawData = io.BytesIO(rawData) #rawData é um arquivo byte, transforma em ioBytes 
        lines = rawData.readlines()   #Com objeto ioBytes tem acesso ao readlines 

        #Header
        #print(lines[0])
        dataLines = lines[0].decode().split(',')  #Lines[0] tem o header Provicia, country, latiture, longitude os dias de 22/01 até atualmente

        for line in lines[1:]:
            data = line.decode().split(',')
            if (data[1] == self.country_name):
                day_c = 0
                for e, cases in enumerate(data[4:]):
                    #Separa o timestamp
                    try:
                        tmp = dataLines[e+4].split('/')
                        tmp = str(tmp[0]+"-"+tmp[1])
                    except:
                        tmp = 'ERRO'
                    #casting
                    try:
                        cases = np.uint64(cases)
                    except:
                        cases = float(cases)
                        cases = np.uint64(cases)
                    finally:
                         #Teste de erro nos dados
                        if(cases > 1000000):
                            cases = 1
                            day_c = 1

                    #coloca em uma lista onde cada linha é uma lista [mm-dd, casosAcumulados, novosCasos]
                    self.DailyCases.append([tmp, cases, int((cases - day_c))])
                    #print(self.country_code, " TimeStamp: ", tmp,"-> Cases: ", cases, "-> Daily New Cases: +", int((int(cases) - day_c)) )
                    day_c = cases
    
    def setData(self):
        #Redebe dados da API (Se retornar sem info é problema no json da API espera normalizar)
        data = self.covid19.getLocationByCountryCode(self.country_code, timelines=True)
        #Pega apenas informações relevantes
        data = data[0]['timelines']['confirmed']['timeline']
        #Retorno é um dicionario, neste caso preferi usar transformar em list
        newData = [ [k,v] for k, v in data.items() ]
        #Pega apartir do dia 21/02 onde começaram surtos na europa por isso o [30:0]
        #Separa a tupla [timestamp, casos] em duas listas
        day_c = 0
        for x,y in newData[30:]:
            print(self.country_code, " TimeStamp: ", x,"-> Cases: ", y, "-> Daily New Cases: +", (y - day_c) )
            #separa o timestamp
            tmp = x.split('-')
            tmp_st =str(tmp[1]+"-"+tmp[2][0:2])
            #coloca em uma lista onde cada linha é uma lista [mm-dd, casosAcumulados, novosCasos]
            self.DailyCases.append([tmp_st, y, (y - day_c)])
            day_c = y
    def setDatabyList(self,data):
        self.DailyCases = list(data)
    def getData(self):
        return self.DailyCases

    def resetData(self):
        self.DailyCases.clear()

def getCountriesList(url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'):
    try:
        rawData=requests.get(url).text.encode()
    except:
        print("Erro de conexão aos Dados...")
        print("FInalizando programa")
        sys.exit()

    rawData = io.BytesIO(rawData) #rawData é um arquivo byte, transforma em ioBytes 
    lines = rawData.readlines()   #Com objeto ioBytes tem acesso ao readlines 
    countries = []
    for line in lines[1:]:
        data = line.decode().split(',')
        if(data[1]=="\"Korea"): data[1]="Korea"
        if(data[1] not in countries): countries.append(data[1])
    return countries

    
# ------------------------- MAIN -------------------------#
#Create a object from API COVID19Py
#Descomente para usar esta API e use a função getData() da classe
'''covid19 = COVID19Py.COVID19()
#latestData = covid19.getLatest()
#print(latestData)'''

#Descomente para 'Criar' o mundo todo criando um objeto para cada país
'''countries = getCountriesList()
world = WorldAgainstCovid19(countries)'''

#Decomente para criar top10 paises de uma vez
#countries = ['US','Spain','Italy','Germany','France','China','Iran','United Kingdom','Turkey','Switzerland']
countries = ['US','Spain','Italy','Germany','France']
top10 = WorldAgainstCovid19(countries)

top10Cases = []
for country in top10.getCountries():
    a = country.getData()
    top10Cases.append(a[-1][-2])
print(top10Cases)
top10.doGraphic(top10Cases)
#Create the objects for the countries and set the data
br = CountryAgainstCovid19(0, "Brazil", "BR","green")
br.setData_URL()

usa = CountryAgainstCovid19(0, "US", "US","red")
usa.setData_URL()

it = CountryAgainstCovid19(0, "Italy", "IT","black")
it.setData_URL()

sp = CountryAgainstCovid19(0, "Spain", "ES","blue")
sp.setData_URL()

#Compute the linear regression for Brazil
br_lr = linearRegressionModel(br, 'Cases')
br_lr.computeModel()
br_lr.doGraphic()
#computeLinearRegression(br)

#Make some nice graphics
doGraphics(br, usa, it, sp)
doBarGraph(br, usa, it, sp)

#### Below we have the ~dark side~ the first implementation awful
'''
#Get the latest data per country
LatestBrazilianData = covid19.getLocationByCountryCode("BR", timelines=True)
LatestUSAData = covid19.getLocationByCountryCode("US", timelines=True)
LatestItalianData = covid19.getLocationByCountryCode("IT", timelines=True)
LatestSpanishData = covid19.getLocationByCountryCode("ES", timelines=True)

#Get timeline per country
#Brazil
BrazilianTimeline = LatestBrazilianData[0]['timelines']['confirmed']['timeline']
#print(BrazilianTimeline)
BrazilianTimelineS = [ [k,v] for k, v in BrazilianTimeline.items() ]

#USA
USATimeline = LatestUSAData[0]['timelines']['confirmed']['timeline']
USATimelineS = [ [k,v] for k, v in USATimeline.items() ]
#print(USATimeline)
#Italy
ItalianTimeline = LatestItalianData[0]['timelines']['confirmed']['timeline']
ItalianTimelineS = [ [k,v] for k, v in ItalianTimeline.items() ]
#print(ItalianTimeline)
#Spain
SpanishTimeline = LatestSpanishData[0]['timelines']['confirmed']['timeline']
SpanishTimelineS = [ [k,v] for k, v in SpanishTimeline.items() ]
#print(SpanishTimeline)

DailyBrazilCases = []
TimeStampBR = []
day_c = 0
for x,y in BrazilianTimelineS[30:]:
    print("BR TimeStamp: ", x,"-> Cases: ", y, "-> Daily New Cases: ", (y - day_c) )
    day_c = y
    #separa o timestap
    tmp = x.split('-')
    tmp_st =str(tmp[1]+"-"+tmp[2][0:2])
    #coloca em uma lista onde cada linha é uma string mm-dd
    TimeStampBR.append(tmp_st)
    DailyBrazilCases.append(y)

DailyUSACases = []
TimeStampUSA = []
for x,y in USATimelineS[30:]:
    #print("USA TimeStamp: ", x,"-> ",y)
    #separa o timestap
    tmp = x.split('-')
    tmp_st =str(tmp[1]+"-"+tmp[2][0:2])
    #coloca em uma lista onde cada linha é uma string mm-dd
    TimeStampUSA.append(tmp_st)
    DailyUSACases.append(y)

DailyItalianCases = []
for x,y in ItalianTimelineS[30:]:
    #print("IT TimeStamp: ", x,"-> ",y)
    DailyItalianCases.append(ItalianTimeline[x])

DailySpanishCases = []
for x,y in SpanishTimelineS[30:]:
    #print("ES TimeStamp: ", x,"-> ",y)
    DailySpanishCases.append(y)

#doGraphics(DailyBrazilCases, DailyUSACases, DailyItalianCases, DailySpanishCases)
doBarGraph(DailyItalianCases, DailySpanishCases, DailyUSACases, DailyBrazilCases, TimeStampBR)
'''