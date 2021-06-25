import pandas as pd
import os
#import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None

def graficiSettimanali():
    covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")

    covid19['data']=(pd.to_datetime(covid19["data"]))
    covid19=covid19.fillna(0)
    print (covid19.info())
    listaDate=list(pd.to_datetime(covid19["data"]))
    for i in range(len(listaDate)):
        listaDate[i]=listaDate[i].strftime("%d-%m-%Y")
    covid19["data"]=listaDate.copy()
    #print("listaDate = "+ str(listaDate))
    covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)

    covid19.set_index("denominazione_regione",inplace=True)
    print(covid19.info())


    listaDatePulita= listaDate[::21] 
    #print(listaDatePulita)


    listaLunedi=listaDatePulita[::7]
    #print("listaLunedi"+str(listaLunedi))

    listaDomeniche=listaDatePulita[6::7]

    #Tasso di positivita ai tamponi totali
    listaSettimanaleTassoDiPositivitaInVeneto=[]
    listaSettimanaleTassoDiPositivitaInItalia=[]


    for i in range(listaDomeniche.index("17-01-2021"), len(listaDomeniche)-1):
      
        tamponiSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi']
        positiviSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['totale_casi'] - covid19[covid19['data']==listaDomeniche[i]]['totale_casi']

        rapportoSettimanale = positiviSettimanali*100/tamponiSettimanali
        rapportoSettimanaleInVeneto= rapportoSettimanale["Veneto"]
        rapportoSettimanaleInItalia = positiviSettimanali.sum()*100/tamponiSettimanali.sum()
        
        listaSettimanaleTassoDiPositivitaInVeneto.append(rapportoSettimanaleInVeneto)
        listaSettimanaleTassoDiPositivitaInItalia.append(rapportoSettimanaleInItalia)



    #Tasso di positivita ai tamponi molecolari
    listaSettimanaleTassoDiPositivitaMolecolareInVeneto=[]
    listaSettimanaleTassoDiPositivitaMolecolareInItalia=[]
    for i in range(listaDomeniche.index("17-01-2021")-1):
        tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi']
        
        positiviMolecolariSettimanali= covid19[covid19['data']==listaDomeniche[i+1]]['totale_casi'] - covid19[covid19['data']==listaDomeniche[i]]['totale_casi']
            
        rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
        rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
        rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()
        listaSettimanaleTassoDiPositivitaMolecolareInVeneto.append(rapportoMolecolareSettimanaleInVeneto)
        listaSettimanaleTassoDiPositivitaMolecolareInItalia.append(rapportoMolecolareSettimanaleInItalia)

    #settimanaMista


    tamponiMolecolariSettimanali = covid19[covid19['data']=='17-01-2021']['tamponi_test_molecolare'] - covid19[covid19['data']=='10-01-2021']['tamponi']
    positiviMolecolariSettimanali = covid19[covid19['data']=='17-01-2021']['totale_positivi_test_molecolare'] - covid19[covid19['data']=='10-01-2021']['totale_casi']
        
    rapportoMolecolareSettimanale= positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali

    rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
    rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()
    listaSettimanaleTassoDiPositivitaMolecolareInVeneto.append(rapportoMolecolareSettimanaleInVeneto)
    listaSettimanaleTassoDiPositivitaMolecolareInItalia.append(rapportoMolecolareSettimanaleInItalia)

    #Settimane dal 15 in poi
    for i in range(listaDomeniche.index("17-01-2021"),len(listaDomeniche)-1):
        tamponiMolecolariSettimanali = covid19[covid19['data']==listaDomeniche[i+1]]['tamponi_test_molecolare'] - covid19[covid19['data']==listaDomeniche[i]]['tamponi_test_molecolare']

        positiviMolecolariSettimanali=covid19[covid19['data']==listaDomeniche[i+1]]['totale_positivi_test_molecolare'] - covid19[covid19['data']==listaDomeniche[i]]['totale_positivi_test_molecolare']
        
        rapportoMolecolareSettimanale = positiviMolecolariSettimanali*100/tamponiMolecolariSettimanali
        rapportoMolecolareSettimanaleInVeneto= rapportoMolecolareSettimanale["Veneto"]
        rapportoMolecolareSettimanaleInItalia = positiviMolecolariSettimanali.sum()*100/tamponiMolecolariSettimanali.sum()
        listaSettimanaleTassoDiPositivitaMolecolareInVeneto.append( rapportoMolecolareSettimanaleInVeneto)
        listaSettimanaleTassoDiPositivitaMolecolareInItalia.append(rapportoMolecolareSettimanaleInItalia)


    #Ingressi in terapia intensiva
    listaSettimanaleTerapiaIntensivaInItalia=[]
    listaSettimanaleTerapiaIntensivaInVeneto=[]
    for i in range(len(listaDomeniche)-1):
        terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva'] - covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']
        terapiaIntensivaSettimanaleInVeneto=terapiaIntensivaSettimanale["Veneto"]
        terapiaIntensivaSettimanaleInItalia=terapiaIntensivaSettimanale.sum()
        listaSettimanaleTerapiaIntensivaInVeneto.append(terapiaIntensivaSettimanaleInVeneto)
        listaSettimanaleTerapiaIntensivaInItalia.append(terapiaIntensivaSettimanaleInItalia/21)
        print(listaDomeniche[i+1] + ':' + str(terapiaIntensivaSettimanaleInItalia/21))
        print(listaDomeniche[i+1] , ':' ,terapiaIntensivaSettimanaleInVeneto)     




    #ospedali non intensiva
    listaSettimanaleOspedaliNonIntensivaInItalia=[]
    listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto=[]
    for i in range(len(listaDomeniche)-1):
        totaleOspedalizzati=covid19[covid19["data"]==listaDomeniche[i+1]]['totale_ospedalizzati']-covid19[covid19["data"]==listaDomeniche[i]]['totale_ospedalizzati']
        terapiaIntensivaSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['terapia_intensiva']-covid19[covid19["data"]==listaDomeniche[i]]['terapia_intensiva']

        ospedalizzatiNonIntensiva=totaleOspedalizzati-terapiaIntensivaSettimanale

        ospedalizzatiNonIntensivaInVeneto=ospedalizzatiNonIntensiva["Veneto"]
        ospedalizzatiNonIntensivaInItalia=ospedalizzatiNonIntensiva.sum()
        listaSettimanaleOspedaliNonIntensivaInItalia.append(ospedalizzatiNonIntensivaInItalia/21)
        listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto.append(ospedalizzatiNonIntensivaInVeneto)
    #print(listaSettimanaleOspedaliNonIntensivaInItalia)
    #print(listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto)





    #deceduti
    listaSettimanaleDecedutiInItalia=[]
    listaSettimanaleDecedutiInVeneto=[]
    for i in range(len(listaDomeniche)-1):
        decedutiSettimanale=covid19[covid19["data"]==listaDomeniche[i+1]]['deceduti']-covid19[covid19["data"]==listaDomeniche[i]]['deceduti']
        decedutiSettimanaleInVeneto=decedutiSettimanale["Veneto"]
        decedutiSettimanaleInItalia=decedutiSettimanale.sum()
        listaSettimanaleDecedutiInVeneto.append(decedutiSettimanaleInVeneto)
        listaSettimanaleDecedutiInItalia.append(decedutiSettimanaleInItalia/21)



    
    '''
    #Grafico per il tasso di positivita ai tamponi totali
    plt.figure(figsize=(16,10))
    italia,=plt.plot(listaDomeniche[listaDomeniche.index("17-01-2021")+1:],listaSettimanaleTassoDiPositivitaInItalia,label="Italia")
    veneto,=plt.plot(listaDomeniche[listaDomeniche.index("17-01-2021")+1:],listaSettimanaleTassoDiPositivitaInVeneto,label="Veneto")
    plt.legend([veneto,italia],["Veneto","Italia"])
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
    plt.xticks(listaDomeniche[listaDomeniche.index("17-01-2021")+1::10])
    plt.title('Tasso di positivita totale')
    plt.xlabel('Date')
    plt.ylabel('Percentuale')
    plt.grid(axis='y')
    plt.show()

    #Grafico per il tasso di positivita ai tamponi totali
    plt.figure(figsize=(16,10))
    italia,=plt.plot(listaDomeniche[1:],listaSettimanaleTassoDiPositivitaMolecolareInItalia,label="Italia")
    veneto,=plt.plot(listaDomeniche[1:],listaSettimanaleTassoDiPositivitaMolecolareInVeneto,label="Veneto")
    plt.legend([veneto,italia],["Veneto","Italia"])
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
    plt.xticks(listaDomeniche[1::10])
    plt.title('Tasso di positivita molecolare')
    plt.xlabel('Date')
    plt.ylabel('Percentuale')
    plt.grid(axis='y')
    plt.show()


    #Grafico intensiva
    plt.figure(figsize=(16,10))
    italia,=plt.plot(listaDomeniche[1:],listaSettimanaleTerapiaIntensivaInItalia,label="Media regionale")
    veneto,=plt.plot(listaDomeniche[1:],listaSettimanaleTerapiaIntensivaInVeneto,label="Veneto")
    plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
    plt.xticks(listaDomeniche[1::10])
    plt.title('Ingressi settimanali in terapia intensiva')
    plt.xlabel('Date')
    plt.ylabel('Nuove terapie intensive')
    plt.grid(axis='y')
    plt.show()

    #grafico ospdali non intensiva
    plt.figure(figsize=(16,10))
    italia,=plt.plot(listaDomeniche[1:],listaSettimanaleOspedaliNonIntensivaInItalia,label="Media regionale")
    veneto,=plt.plot(listaDomeniche[1:],listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto,label="Veneto")
    plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
    plt.xticks(listaDomeniche[1::10])
    plt.title('Ingressi giornalieri in ospendale non in terapia intensiva')
    plt.xlabel('Date')
    plt.ylabel('Nuovi ospedalizzati non intensiva')
    plt.grid(axis='y')
    plt.show()


    #deceduti grafico
    plt.figure(figsize=(16,10))
    italia,=plt.plot(listaDomeniche[1:],listaSettimanaleDecedutiInItalia,label="Media regionale")
    veneto,=plt.plot(listaDomeniche[1:],listaSettimanaleDecedutiInVeneto,label="Veneto")
    plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
    plt.xticks(listaDomeniche[1::10])
    plt.title('Deceduti settimanali')
    plt.xlabel('Date')
    plt.ylabel('Nuovi ospedalizzati non intensiva')
    plt.grid(axis='y')
    plt.show()
    '''
    


    #CSV CON TUTTI I DATI (ESCLUSI I TAMPONI TOTALI)

    covid19PerGraficiSettimanaliItaliaVeneto=pd.DataFrame({"Data":listaDomeniche[1:]})
    covid19PerGraficiSettimanaliItaliaVeneto['Tasso di positivita ai tamponi molecolari Italia']=listaSettimanaleTassoDiPositivitaMolecolareInItalia
    covid19PerGraficiSettimanaliItaliaVeneto['Tasso di positivita ai tamponi molecolari Veneto']=listaSettimanaleTassoDiPositivitaMolecolareInVeneto
    covid19PerGraficiSettimanaliItaliaVeneto['Ingressi in terapia intensiva Media Regionale']=listaSettimanaleTerapiaIntensivaInItalia
    covid19PerGraficiSettimanaliItaliaVeneto['Ingressi in terapia intensiva Veneto']=listaSettimanaleTerapiaIntensivaInVeneto
    covid19PerGraficiSettimanaliItaliaVeneto['Ingressi nei reparti ordinari Media Regionale']=listaSettimanaleOspedaliNonIntensivaInItalia
    covid19PerGraficiSettimanaliItaliaVeneto['Ingressi nei reparti ordinari Veneto']=listaSettimanaleOspedaliNonTerapiaIntensivaInVeneto
    covid19PerGraficiSettimanaliItaliaVeneto['Deceduti Media Regionale']=listaSettimanaleDecedutiInItalia
    covid19PerGraficiSettimanaliItaliaVeneto['Deceduti Veneto']=listaSettimanaleDecedutiInVeneto
    
    if os.path.exists("csv/Covid19GraficiSettimanaliItaliaVeneto.csv"):
	    os.remove("csv/Covid19GraficiSettimanaliItaliaVeneto.csv")

    covid19PerGraficiSettimanaliItaliaVeneto.to_csv("csv/Covid19GraficiSettimanaliItaliaVeneto.csv",index=False)


    #CSV per i soli tamponi totali
    covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali=pd.DataFrame({"Data":listaDomeniche[listaDomeniche.index("24-01-2021"):]})
    covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali['Tasso di positivita ai tamponi totali Italia']=listaSettimanaleTassoDiPositivitaInItalia
    covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali['Tasso di positivita ai tamponi totali Veneto']=listaSettimanaleTassoDiPositivitaInVeneto

    if os.path.exists("csv/Covid19GraficiSettimanaliTamponiTotaliItaliaVeneto.csv"):
	    os.remove("csv/Covid19GraficiSettimanaliTamponiTotaliItaliaVeneto.csv")

    covid19PerGraficiSettimanaliItaliaVenetoTamponiTotali.to_csv("csv/Covid19GraficiSettimanaliTamponiTotaliItaliaVeneto.csv",index=False)