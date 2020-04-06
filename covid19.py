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
import requests

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
# @param: c1 is the countries object
# @return: void
def computeLinearRegression(c1):
    from sklearn import linear_model

    X = np.array(range(len(c1.getData()))).reshape((-1, 1))
    #print(X)
    y = np.array([v for k,v,f in c1.getData()])
    #print(y)

    #create the LinearRegression model
    clf = LinearRegression()

    #train model
    clf.fit(X, y)
    # 4. Avalia o modelo
    print('coeficiente de determinação:', clf.score(X, y))

    # Intercept
    print('intercept:', clf.intercept_)
    
    # Slope
    print('slope:', clf.coef_)

    # 5. Cria um novo conjunto de dados x. Arange gera um array com elementos de 0(inclusivo) a 5 (exclusivo)
    novo_x = np.arange(5).reshape((-1, 1))
    print(novo_x)

    # 6. Aplica o modelo num novo conjunto de dados
    previsao_y = clf.predict(novo_x)
    print(previsao_y)


#class WorldAgainsCovid19():
#    def __init__(self):
#        self.country_name = ""
#        self.DailyCases = []
# @brief: Object from country, we have a setData function which one receive dada from API and set into the class and getData return this data as a list
# @param: covid19 is the API object
# @param: name is the country name such as Brazil
# @param: code is the country code such as BR, US, IT
# @param: color is a arbitrary color for the graphics
class CountryAgainstCovid19():
    def __init__(self, covid19, name, code, color):
        self.country_name = name
        self.country_code = code
        self.country_color = color
        self.covid19 = covid19
        self.DailyCases = []
        
    def setData_URL(self, url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'):
        rawData=requests.get(url).text.encode()
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
                    tmp = dataLines[e+4].split('/')
                    tmp = str(tmp[0]+"-"+tmp[1])
                    #casting
                    cases = int(cases)
                    #coloca em uma lista onde cada linha é uma lista [mm-dd, casosAcumulados, novosCasos]
                    self.DailyCases.append([tmp, cases, (cases - day_c)])
                    print(self.country_code, " TimeStamp: ", tmp,"-> Cases: ", cases, "-> Daily New Cases: +", (int(cases) - day_c) )
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
    def getData(self):
        return self.DailyCases

    def resetData(self):
        self.DailyCases.clear()

# ------------------------- MAIN -------------------------#
#Create a object from API COVID19Py
covid19 = COVID19Py.COVID19()
latestData = covid19.getLatest()
print(latestData)

#Create the objects for the countries and set the data
br = CountryAgainstCovid19(covid19, "Brazil", "BR","green")
br.setData_URL()

usa = CountryAgainstCovid19(covid19, "US", "US","red")
usa.setData_URL()

it = CountryAgainstCovid19(covid19, "Italy", "IT","black")
it.setData_URL()

sp = CountryAgainstCovid19(covid19, "Spain", "ES","blue")
sp.setData_URL()

#Compute the linear regression for Brazil
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