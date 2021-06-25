#Ora facciamo i grafici dei valori giornalieri giorno dopo giorno da inizio pandemia

import math
import pandas as pd
pd.options.mode.chained_assignment = None
import os

def graficiGiornalieri():

	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")

	covid19['data']=(pd.to_datetime(covid19["data"]))
	covid19=covid19.fillna(0)

	listaDate=list(pd.to_datetime(covid19["data"]))
	for i in range(len(listaDate)):
		listaDate[i]=listaDate[i].strftime("%d-%m-%Y")
	covid19["data"]=listaDate.copy()

	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)

	covid19.set_index("denominazione_regione",inplace=True)
	#print(covid19.info())

	#Prendiamo tutte le date da inizio pandemia
	date=covid19["data"]
	quanteDateCiSonoState=len(date)//21
	#print(quanteDateCiSonoState)
	listaDate=[]
	for i in range(quanteDateCiSonoState):
		listaDate.append(date[-21*i-1])
	listaDate.reverse()
	#print(listaDate)


	#Prendiamo il dataframe al primo giorno di pandemia
	covid19PrimoGiorno=covid19[covid19["data"]==listaDate[0]]






	#Positivi su tamponi molecolari giornalieri
	rapportoPositiviSuTamponiMolecolariGiornalieri=[]
	rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto=[]
	dateRilevanti=[]
	dateRilevantiVeneto=[]
	tamponiMolecolariPrimoGiorno=covid19PrimoGiorno["tamponi"]
	tamponiMolecolariPrimoGiornoInVeneto=tamponiMolecolariPrimoGiorno["Veneto"]
	nuoviPositiviMolecolariPrimoGiorno=covid19PrimoGiorno["nuovi_positivi"]
	nuoviPositiviMolecolariPrimoGiornoInVeneto=nuoviPositiviMolecolariPrimoGiorno["Veneto"]
	tassoPositiviSuTamponiMolecolariPrimoGiorno=nuoviPositiviMolecolariPrimoGiorno.sum()*100/tamponiMolecolariPrimoGiorno.sum()
	tassoPositiviSuTamponiMolecolariPrimoGiornoInVeneto=nuoviPositiviMolecolariPrimoGiornoInVeneto*100/tamponiMolecolariPrimoGiornoInVeneto
	rapportoPositiviSuTamponiMolecolariGiornalieri.append(tassoPositiviSuTamponiMolecolariPrimoGiorno)
	rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto.append(tassoPositiviSuTamponiMolecolariPrimoGiornoInVeneto)


	for i in range(1, quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]

		if math.floor(covid19UltimoGiorno["tamponi_test_molecolare"][0])==0:
			pass
		else:
			inizioDate=i
			break

	#print(inizioDate)

	for i in range(inizioDate, quanteDateCiSonoState):
		dateRilevanti.append(listaDate[i])
		dateRilevantiVeneto.append(listaDate[i])

	for i in range(1,inizioDate):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
		tamponiMolecolariEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
		tamponiMolecolariEffettuatuUltimoGiornoInVeneto=tamponiMolecolariEffettuatuUltimoGiorno["Veneto"]
		tamponiMolecolariEffettuatuUltimoGiornoTotale=tamponiMolecolariEffettuatuUltimoGiorno.sum()
		
		nuoviPositiviMolecolariUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]
		nuoviPositiviMolecolariUltimoGiornoInVeneto=nuoviPositiviMolecolariUltimoGiorno["Veneto"]
		nuoviPositiviMolecolariUltimoGiornoInItalia=nuoviPositiviMolecolariUltimoGiorno.sum()

		tassoPositiviSuTamponiMolecolariGiornalieri=nuoviPositiviMolecolariUltimoGiornoInItalia*100/tamponiMolecolariEffettuatuUltimoGiornoTotale
		tassoPositiviSuTamponiMolecolariGiornalieriInVeneto=nuoviPositiviMolecolariUltimoGiornoInVeneto*100/tamponiMolecolariEffettuatuUltimoGiornoInVeneto

		rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto.append(tassoPositiviSuTamponiMolecolariGiornalieriInVeneto)
		rapportoPositiviSuTamponiMolecolariGiornalieri.append(tassoPositiviSuTamponiMolecolariGiornalieri)
		
	for i in range(inizioDate,quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
		tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi_test_molecolare"]
		
		tamponiMolecolariUltimoGiornoInVeneto=tamponiMolecolariUltimoGiorno["Veneto"]
		nuoviPositiviMolecolare=covid19UltimoGiorno["totale_positivi_test_molecolare"]-covid19PenultimoGiorno["totale_positivi_test_molecolare"]
		nuoviPositiviMolecolareInVeneto=nuoviPositiviMolecolare["Veneto"]
		tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
		tassoPositiviMolecolariInVeneto=nuoviPositiviMolecolareInVeneto*100/tamponiMolecolariUltimoGiornoInVeneto
		tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()
		
		rapportoPositiviSuTamponiMolecolariGiornalieri.append(tassoNazionalePositiviMolecolari)
		rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto.append(tassoPositiviMolecolariInVeneto)
		

	#print(rapportoPositiviSuTamponiMolecolariGiornalieri)

	#Positivi su tamponi totali giornalieri, dato italiano e dato veneto. 
	rapportoPositiviSuTotaleTamponiGiornalieri=[]
	rapportoPositiviSuTotaleTamponiGiornalieriInVeneto=[]

	for i in range(quanteDateCiSonoState-len(dateRilevanti)):
		rapportoPositiviSuTotaleTamponiGiornalieri.append(0)
		rapportoPositiviSuTotaleTamponiGiornalieriInVeneto.append(0)

	for i in range(quanteDateCiSonoState-len(dateRilevanti),quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
		tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
		tamponiEffettuatuUltimoGiornoInVeneto=tamponiEffettuatuUltimoGiorno["Veneto"]
		
		tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
		nuoviPositiviUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]
		nuoviPositiviUltimoGiornoInVeneto=nuoviPositiviUltimoGiorno["Veneto"]
		nuoviPositiviUltimoGiornoInItalia=nuoviPositiviUltimoGiorno.sum()

		rapportoPositiviSuTotaleTamponiUltimoGiorno=nuoviPositiviUltimoGiorno*100/tamponiEffettuatuUltimoGiorno
		rapportoPositiviSuTotaleTamponiUltimoGiornoInVeneto=rapportoPositiviSuTotaleTamponiUltimoGiorno["Veneto"]
		rapportoPositiviSuTotaleTamponiGiornalieriInVeneto.append(rapportoPositiviSuTotaleTamponiUltimoGiornoInVeneto)

		covid19UltimoGiorno["ultimo_giorno_rapporto_positivi_tamponi"]=rapportoPositiviSuTotaleTamponiUltimoGiorno
		rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale
		rapportoPositiviSuTotaleTamponiGiornalieri.append(rapportoPositiviTamponiUltimoGiornoInItalia)
	#print(rapportoPositiviSuTotaleTamponiGiornalieri)



	#INGRESSI GIORNALIERI IN TERAPIA INTENSIVA
	ingressiIntensivaGiornalieri=[]
	ingressiIntensivaGiornalieriInVeneto=[]

	ingressiPrimoGiornoTerapiaIntensiva=covid19PrimoGiorno["terapia_intensiva"]
	ingressiPrimoGiornoTerapiaIntensivaInVeneto=ingressiPrimoGiornoTerapiaIntensiva["Veneto"]
	ingressiPrimoGiornoTerapiaIntensivaInItalia=ingressiPrimoGiornoTerapiaIntensiva.sum()
	ingressiIntensivaGiornalieri.append(ingressiPrimoGiornoTerapiaIntensivaInItalia/21.0)
	ingressiIntensivaGiornalieriInVeneto.append(ingressiPrimoGiornoTerapiaIntensivaInVeneto)
	for i in range(1,quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
		ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
		ingressiUltimoGiornoTerapiaIntensivaInVeneto=ingressiUltimoGiornoTerapiaIntensiva["Veneto"]
		ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
		ingressiIntensivaGiornalieri.append(ingressiUltimoGiornoTerapiaIntensivaInItalia/21.0)
		ingressiIntensivaGiornalieriInVeneto.append(ingressiUltimoGiornoTerapiaIntensivaInVeneto)
	#print(ingressiIntensivaGiornalieri)


	#INGRESSI GIORNALIERI NON IN TERAPIA INTENSIVA
	ingressiNonIntensivaGiornalieri=[]
	ingressiNonIntensivaGiornalieriInVeneto=[]

	ingressiOspedaleCompresaTerapiaIntensivaPrimoGiorno=covid19PrimoGiorno["totale_ospedalizzati"]
	ingressiNonIntensivaPrimoGiorno=ingressiOspedaleCompresaTerapiaIntensivaPrimoGiorno-ingressiPrimoGiornoTerapiaIntensiva
	ingressiNonIntensivaPrimoGiornoInVeneto=ingressiNonIntensivaPrimoGiorno["Veneto"]
	ingressiNonIntensivaPrimoGiornoInItalia=ingressiNonIntensivaPrimoGiorno.sum()
	ingressiNonIntensivaGiornalieri.append(ingressiNonIntensivaPrimoGiornoInItalia/21.0)
	ingressiNonIntensivaGiornalieriInVeneto.append(ingressiNonIntensivaPrimoGiornoInVeneto)

	for i in range(1,quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
		ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19PenultimoGiorno["totale_ospedalizzati"]
		#print(str(ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva.sum()) +"   "+str(ingressiIntensivaGiornalieri[i-1]))
		ingressiUltimoGiornoOspedaleCompresaTerapiaIntensivaInVeneto=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva["Veneto"]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensivaInVeneto-ingressiIntensivaGiornalieriInVeneto[i]
		ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva.sum()-ingressiIntensivaGiornalieri[i-1]
		ingressiNonIntensivaGiornalieriInVeneto.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInVeneto)
		ingressiNonIntensivaGiornalieri.append(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva/21.0)
	#print(ingressiNonIntensivaGiornalieri)


	#DECEDUTI 
	deceduti=[]
	decedutiInVeneto=[]
	decedutiPrimoGiorno=covid19PrimoGiorno["deceduti"]
	decedutiPrimoGiornoInVeneto=decedutiPrimoGiorno["Veneto"]
	decedutiPrimoGiornoInItalia=decedutiPrimoGiorno.sum()
	decedutiInVeneto.append(decedutiPrimoGiornoInVeneto)
	deceduti.append(decedutiPrimoGiornoInItalia)

	for i in range(1,quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
		decedutiUltimoGiornoInVeneto=(covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"])["Veneto"]


		decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"].sum()-covid19PenultimoGiorno["deceduti"].sum()
		deceduti.append(decedutiUltimoGiorno/21.0)
		decedutiInVeneto.append(decedutiUltimoGiornoInVeneto)
	#print (deceduti)


	#LETALITA
	letalita=[]
	letalitaInVeneto=[]
	tassoDiMortalitaPrimoGiorno=covid19PrimoGiorno["deceduti"]*100/covid19PrimoGiorno["totale_casi"]
	tassoDiMortalitaPrimoGiornoInVeneto=tassoDiMortalitaPrimoGiorno["Veneto"]
	tassoDiMortalitaNazionalePrimoGiorno=covid19PrimoGiorno["deceduti"].sum()*100/covid19PrimoGiorno["totale_casi"].sum()
	letalitaInVeneto.append(tassoDiMortalitaPrimoGiornoInVeneto)
	letalita.append(tassoDiMortalitaNazionalePrimoGiorno)

	for i in range(1,quanteDateCiSonoState):
		covid19UltimoGiorno=covid19[covid19["data"]==listaDate[i]]
		covid19PenultimoGiorno=covid19[covid19["data"]==listaDate[i-1]]
		tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
		tassoDiMortalitaInVeneto=tassoDiMortalita["Veneto"]
		tassoDiMortalitaNazionale=covid19UltimoGiorno["deceduti"].sum()*100/covid19UltimoGiorno["totale_casi"].sum()
		letalitaInVeneto.append(tassoDiMortalitaInVeneto)
		letalita.append(tassoDiMortalitaNazionale)
	#print (letalita)


	#Grafico positivi test molecolari
	'''
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto,label="Veneto")
	italia,=plt.plot(listaDate,rapportoPositiviSuTamponiMolecolariGiornalieri,label="Italia")
	plt.legend([veneto,italia],["Veneto","Italia"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)

	plt.xticks(listaDate[1::30])

	plt.title('Tasso di positivita giornaliero ai tamponi molecolari da inizio pandemia')
	plt.xlabel('Date')
	plt.ylabel('Tasso di positivita')
	plt.grid(axis='y')
	plt.show()

	#Grafico positivi test totali
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,rapportoPositiviSuTotaleTamponiGiornalieriInVeneto,label="Veneto")
	italia,=plt.plot(listaDate,rapportoPositiviSuTotaleTamponiGiornalieri,label="Italia")
	plt.legend([veneto,italia],["Veneto","Italia"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)

	plt.xticks(listaDate[1::30])
	plt.title('Tasso di positivita giornaliero a tutti i tamponi dal 15 gennaio')
	plt.xlabel('Date')
	plt.ylabel('Tasso di positivita')
	plt.grid(axis='y')
	plt.show()




	#Grafico intensiva

	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,ingressiIntensivaGiornalieriInVeneto,label="Veneto")
	italia,=plt.plot(listaDate,ingressiIntensivaGiornalieri,label="Media \nRegionale")
	plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDate[1::30])
	plt.title('Ingressi giornalieri in terapia intensiva')
	plt.xlabel('Date')
	plt.ylabel('Nuove terapie intensive')
	plt.grid(axis='y')
	plt.show()


	#Grafico non intensiva
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,ingressiNonIntensivaGiornalieriInVeneto,label="Veneto")
	italia,=plt.plot(listaDate,ingressiNonIntensivaGiornalieri,label="Media \nRegionale")
	plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDate[1::30])
	plt.title('Ingressi giornalieri in ospendale non in terapia intensiva')
	plt.xlabel('Date')
	plt.ylabel('Nuovi ospedalizzati non intensivi')
	plt.grid(axis='y')
	plt.show()

	#Grafico deceduti
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,decedutiInVeneto,label="Veneto") 
	italia,=plt.plot(listaDate,deceduti,label="Media \nRegionale")
	plt.legend([veneto,italia],["Veneto","Media \nRegionale"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDate[1::30])
	plt.title('Deceduti giornalieri')
	plt.xlabel('Date')
	plt.ylabel('Deceduti')
	plt.grid(axis='y')
	plt.show()

	#Grafico letalita
	plt.figure(figsize=(16,10))
	veneto,=plt.plot(listaDate,letalitaInVeneto,label="Veneto")
	italia,=plt.plot(listaDate,letalita,label="Italia")
	plt.legend([veneto,italia],["Veneto","Italia"])
	plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0)
	plt.xticks(listaDate[1::30])
	plt.title('Tasso di letalita da inizio pandemia')
	plt.xlabel('Date')
	plt.ylabel('Letalita')
	plt.grid(axis='y')
	plt.show()

	'''
	#Creazione database per flourish
	covid19PerGraficiGiornalieriItaliaVeneto=pd.DataFrame({"Data":listaDate})


	covid19PerGraficiGiornalieriItaliaVeneto["Positivi su totale tamponi molecolari in Italia"]=rapportoPositiviSuTamponiMolecolariGiornalieri
	covid19PerGraficiGiornalieriItaliaVeneto["Positivi su totale tamponi molecolari in Veneto"]=rapportoPositiviSuTamponiMolecolariGiornalieriInVeneto



	covid19PerGraficiGiornalieriItaliaVeneto["ingressiTerapiaIntensivaInItalia"]=ingressiIntensivaGiornalieri
	covid19PerGraficiGiornalieriItaliaVeneto["ingressiTerapiaIntensivaInVeneto"]=ingressiIntensivaGiornalieriInVeneto
	covid19PerGraficiGiornalieriItaliaVeneto["ingressi non terapia intensiva in Italia"]=ingressiNonIntensivaGiornalieri
	covid19PerGraficiGiornalieriItaliaVeneto["ingressi non terapia intensiva in Veneto"]=ingressiNonIntensivaGiornalieriInVeneto


	covid19PerGraficiGiornalieriItaliaVeneto["Morti media regionale"]= deceduti
	covid19PerGraficiGiornalieriItaliaVeneto["Morti Veneto"]=decedutiInVeneto
	covid19PerGraficiGiornalieriItaliaVeneto["Letalita italiana"]=letalita
	covid19PerGraficiGiornalieriItaliaVeneto["Letalita Veneta"]=letalitaInVeneto


	#Creazione database con le sole date in cui nel conteggio hanno aggiunto i tamponi rapidi
	covid19PerGraficiTamponiTotali=pd.DataFrame({"Data":dateRilevanti})
	covid19PerGraficiTamponiTotali["Positivi su totale tamponi in Italia"]=rapportoPositiviSuTotaleTamponiGiornalieri[quanteDateCiSonoState-len(dateRilevanti):]
	covid19PerGraficiTamponiTotali["Positivi su totale tamponi in Veneto"]=rapportoPositiviSuTotaleTamponiGiornalieriInVeneto[quanteDateCiSonoState-len(dateRilevanti):]


	if os.path.exists("csv/Covid19GraficiItaliaEVeneto.csv"):
	    os.remove("csv/Covid19GraficiItaliaEVeneto.csv")
	
	df1=covid19PerGraficiGiornalieriItaliaVeneto.to_csv(sep=",",index=False)


	if os.path.exists("csv/Covid19GraficiTamponiTotaliItaliaEVeneto.csv"):
	    os.remove("csv/Covid19GraficiTamponiTotaliItaliaEVeneto.csv")

	df2=covid19PerGraficiTamponiTotali.to_csv(sep=",",index=False)


	#Codice per commitare su Gthub
	from github import Github, InputGitTreeElement
	from datetime import date

	fileList=[df1,df2]
	fileNames=["Covid19GraficiItaliaEVeneto.csv","Covid19GraficiTamponiTotaliItaliaEVeneto.csv"]

	commitMessage=date.today().strftime("%d-%m-%Y")

	g=Github("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")

	#Prendo cartella
	'''
	for repo in g.get_user().get_repos():
		print(repo.name)
		#repo.edit(has_wiki=False)
	'''

	#creo connessione
	repo=g.get_user().get_repo("Covid")
	#print("Sono la cartella", repo)

	'''
	x=repo.get_contents("")
	for labels in x:
		print("label",labels)
	'''
	#file1=repo.get_contents("csv/Covid19GraficiItaliaEVeneto.csv")
	#file2=repo.get_contents("csv/Covid19GraficiTamponiTotaliItaliaEVeneto.csv")

	file1= repo.get_git_refs()
	for y in file1:
		print("y",y)

	mainRef= repo.get_git_ref("heads/main")


	#carichiamo il file

	mainSha=mainRef.object.sha
	baseTree= repo.get_git_tree(mainSha)

	elementList=[]
	for i in range(len(fileList)):
		element=InputGitTreeElement(fileNames[i],'100644','blob',fileList[i])#100644 è per file normale, 'blob' binary large object per caricare su gihub file
		elementList.append(element)

	tree=repo.create_git_tree(elementList, baseTree)
	parent=repo.get_git_commit(mainSha)

	commit=repo.create_git_commit(commitMessage,tree,[parent])
	mainRef.edit(commit.sha)
	print("Aggiornamento completato")





