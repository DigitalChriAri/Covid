import pandas as pd
#import matplotlib.pyplot as plt
import os
pd.options.mode.chained_assignment = None


def mappa():

	covid19 = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",sep=",")



	covid19['data']=(pd.to_datetime(covid19["data"]))
	covid19=covid19.fillna(0)
	print (covid19.info())
	listaDate=list(pd.to_datetime(covid19["data"]))
	for i in range(len(listaDate)):
		listaDate[i]=listaDate[i].strftime("%d-%m-%Y")
	covid19["data"]=listaDate.copy()

	print(covid19.columns)
	print(covid19.info())
	print("\n \n \n \nEcco a voi le note casi:    \n\n\n")
	print(list(covid19["note_casi"]))
	print("\n \n \n \nEcco a voi le note:    \n\n\n")

	print(list(covid19["note"]))
	print("\n \n \n \nEcco a voi le note test:    \n\n\n")
	print(list(covid19["note_test"]))

	covid19.drop(["stato","codice_regione","lat","long","codice_nuts_1", "codice_nuts_2","note","note_test","note_casi"], axis=1, inplace=True)

	covid19.set_index("denominazione_regione",inplace=True)
	#print(covid19.info())

	date=covid19["data"]
	ultimoGiorno=date[-1]
	penultimoGiorno=date[-22]
	unaSettimanaFa=date[-21*7-1]
	covid19UltimoGiorno=covid19[covid19["data"]==ultimoGiorno]
	covid19PenultimoGiorno=covid19[covid19["data"]==penultimoGiorno]
	covid19UnaSettimanaFa=covid19[covid19["data"]==unaSettimanaFa]



	#Rapporto positivi su totale tamponi effettuati ultimo giorno
	tamponiEffettuatuUltimoGiorno=covid19UltimoGiorno["tamponi"]-covid19PenultimoGiorno["tamponi"]
	tamponiEffettuatuUltimoGiornoTotale=tamponiEffettuatuUltimoGiorno.sum()
	#print(tamponiEffettuatuUltimoGiorno)
	#print(tamponiEffettuatuUltimoGiornoTotale)
	nuoviPositiviUltimoGiornoInItalia=covid19UltimoGiorno["nuovi_positivi"].sum()
	#print(nuoviPositiviUltimoGiornoInItalia)
	rapportoPositiviSuTotaleTamponiUltimoGiorno=covid19UltimoGiorno["nuovi_positivi"]*100/tamponiEffettuatuUltimoGiorno
	#print(rapportoPositiviSuTotaleTamponiUltimoGiorno)
	#print(covid19.info())
	rapportoPositiviTamponiUltimoGiornoInItalia=nuoviPositiviUltimoGiornoInItalia*100/tamponiEffettuatuUltimoGiornoTotale
	#print("\n\n\nRapporto positivi tamponi totali ultimo giorno regione per regione")
	#print(rapportoPositiviSuTotaleTamponiUltimoGiorno)
	#print ("Nell'ultima giornata il rapporto positivi/tamponi totali e del " +str(rapportoPositiviTamponiUltimoGiornoInItalia)+"%")


	#Rapporto positivi su tamponi molecolari ultimo giorno
	tamponiMolecolariUltimoGiorno=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19PenultimoGiorno["tamponi_test_molecolare"]
	nuoviPositiviMolecolare=covid19UltimoGiorno["totale_positivi_test_molecolare"]-covid19PenultimoGiorno["totale_positivi_test_molecolare"]
	tassoPositiviMolecolari=nuoviPositiviMolecolare*100/tamponiMolecolariUltimoGiorno
	#print("\n\n\nTasso di positivita al tampone molecolare ultimo giorno regione per regione")
	#print(tassoPositiviMolecolari)
	tassoNazionalePositiviMolecolari=nuoviPositiviMolecolare.sum()*100/tamponiMolecolariUltimoGiorno.sum()
	#print("Il tasso di positivita ai tamponi molecolari nell'ultima giornata e pari al "+str(tassoNazionalePositiviMolecolari)+"%")




	#Ingressi ultimo giorno in terapia intensiva
	ingressiUltimoGiornoTerapiaIntensiva=covid19UltimoGiorno["terapia_intensiva"]-covid19PenultimoGiorno["terapia_intensiva"]
	#print("\n\n\nReparti terapia intensiva ultimo giorno regione per regione")
	#print (ingressiUltimoGiornoTerapiaIntensiva)
	ingressiUltimoGiornoTerapiaIntensivaInItalia=ingressiUltimoGiornoTerapiaIntensiva.sum()
	valore="un incremento"
	if ingressiUltimoGiornoTerapiaIntensivaInItalia<0:
		valore="una riduzione"

	#print("Rispetto a ieri oggi le terapie intensive segnano " +valore+" di "+str(abs(ingressiUltimoGiornoTerapiaIntensivaInItalia))+" unita")

	#Ingressi ospedalieri ultimo giorno NON in terapia intensiva
	ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19PenultimoGiorno["totale_ospedalizzati"]
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva=ingressiUltimoGiornoOspedaleCompresaTerapiaIntensiva-ingressiUltimoGiornoTerapiaIntensiva
	#print("\n\n\nReparti non terapia intensiva ultimo giorno regione per regione")
	#print(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva)
	ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva.sum()
	valore="un incremento"
	if ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia<0:
		valore="una riduzione"
	#print("Rispetto a ieri oggi i reparti non in terapia intensive segnano " +valore+" di "+str(abs(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia))+" unita")


	#Morti ultimo giorno
	decedutiUltimoGiorno=covid19UltimoGiorno["deceduti"]-covid19PenultimoGiorno["deceduti"]

	#Vediamo l'andamento nell'ultima settimana  
	#Rapporto positivi su tamponi totali
	tamponiEffettuatiUltimaSettimana=covid19UltimoGiorno["tamponi"]-covid19UnaSettimanaFa["tamponi"]
	tamponiEffettuatiUltimaSettimanaTotale=tamponiEffettuatiUltimaSettimana.sum()
	#print(tamponiEffettuatiUltimaSettimana)
	#print(tamponiEffettuatiUltimaSettimanaTotale)
	#print(covid19UnaSettimanaFa.info())



	nuoviPositiviUltimaSettimana=0
	for i in range(7):
		nuoviPositiviUltimaSettimana += covid19[covid19["data"]==date[i*(-21)-1]]["nuovi_positivi"]
	nuoviPositiviUltimaSettimanaItalia=nuoviPositiviUltimaSettimana.sum()


	rapportoPositiviUltimaSettimana=nuoviPositiviUltimaSettimana*100/tamponiEffettuatiUltimaSettimana
	#print("\n\n\nRapporto positivi/tamponi totali ultima settimana regione per regione")
	#print(rapportoPositiviUltimaSettimana)
	rapportoPositiviUltimaSettimanaInItalia=nuoviPositiviUltimaSettimanaItalia*100/tamponiEffettuatiUltimaSettimanaTotale
	#print("Nell'ultima settimana in Italia abbiamo avuto un tasso di positivita a tutti i tamponi pari al "+str(rapportoPositiviUltimaSettimanaInItalia)+"%")



	#Tasso di positivita ai molecolari ultima settimana
	tamponiMolecolariEffettuatiUltimaSettimana=covid19UltimoGiorno["tamponi_test_molecolare"]-covid19UnaSettimanaFa["tamponi_test_molecolare"]
	positiviMolecolariUltimaSettimana=covid19UltimoGiorno["totale_positivi_test_molecolare"]-covid19UnaSettimanaFa["totale_positivi_test_molecolare"]
	tassoPositiviMolecolariUltimaSettimana=positiviMolecolariUltimaSettimana*100/tamponiMolecolariEffettuatiUltimaSettimana
	#print("\n\n\nRegione per regione tasso settimanale di positivita ai test molecolari")
	#print(tassoPositiviMolecolariUltimaSettimana)
	tassoNazionalePositiviMolecolariUltimaSettimana=positiviMolecolariUltimaSettimana.sum()*100/tamponiMolecolariEffettuatiUltimaSettimana.sum()
	#print("Nell'ultima settimana in Italia abbiamo avuto un tasso di positivita ai tamponi MOLECOLARI pari al "+str(tassoNazionalePositiviMolecolariUltimaSettimana)+"%")

	#Ingresso terapie intensive ultima settimana
	nuoveTerapieIntensiveUltimaSettimana=covid19UltimoGiorno["terapia_intensiva"]-covid19UnaSettimanaFa["terapia_intensiva"]
	#print("\n\n\nRegione per regione le terapie intensive rispetto a una settimana fa")
	#print(nuoveTerapieIntensiveUltimaSettimana)
	nuoveTerapieIntensiveUltimaSettimanaItalia=nuoveTerapieIntensiveUltimaSettimana.sum()
	valore="un incremento"
	if nuoveTerapieIntensiveUltimaSettimanaItalia<0:
		valore="una riduzione"
	#print("Rispetto a una settimana fa le terapie intensive segnano " +valore+" di "+str(abs(nuoveTerapieIntensiveUltimaSettimanaItalia))+" unita")


	#Ingresso non terapie intensive ultima settimana
	ingressiUltimaSettimaneOspedaleCompresaTerapiaIntensiva=covid19UltimoGiorno["totale_ospedalizzati"]-covid19UnaSettimanaFa["totale_ospedalizzati"]
	ingressiUltimaSettimanaOspedaleSenzaTerapiaIntensiva=ingressiUltimaSettimaneOspedaleCompresaTerapiaIntensiva-nuoveTerapieIntensiveUltimaSettimana
	#print("\n\n\nReparti non terapia intensiva ultima settimana regione per regione")
	#print(ingressiUltimaSettimanaOspedaleSenzaTerapiaIntensiva)
	ingressiUltimaSettimanaOspedaleSenzaTerapiaIntensivaInItalia=ingressiUltimaSettimanaOspedaleSenzaTerapiaIntensiva.sum()
	valore="un incremento"
	if ingressiUltimaSettimanaOspedaleSenzaTerapiaIntensivaInItalia<0:
		valore="una riduzione"
	#print("Rispetto a una settimana fa i reparti non in terapia intensive segnano " +valore+" di "+str(abs(ingressiUltimaSettimanaOspedaleSenzaTerapiaIntensivaInItalia))+" unita")




	#Morti ultima settimana
	decedutiUltimaSettimana=covid19UltimoGiorno["deceduti"]-covid19UnaSettimanaFa["deceduti"]

	#Letalita pandemia 
	tassoDiMortalita=covid19UltimoGiorno["deceduti"]*100/covid19UltimoGiorno["totale_casi"]
	#print("\n\n\n Tasso di mortalita regione per regione")
	#print(tassoDiMortalita)
	tassoDiMortalitaNazionale=covid19UltimoGiorno["deceduti"].sum()*100/covid19UltimoGiorno["totale_casi"].sum()
	#print("Da inizio pandemia il rapporto tra morti e positivi e del "+str(tassoDiMortalitaNazionale)+"%")



	#print("\n\n\n\n\n\n\n")
	#print("Dati del giorno "+ str(list(covid19UltimoGiorno["data"])[0]))
	#print("Rapporto positivi/tamponi ultimo giorno = %.2f" % rapportoPositiviTamponiUltimoGiornoInItalia+"%")
	#print("Rapporto positivi/tamponi ultima settimana =%.2f" %rapportoPositiviUltimaSettimanaInItalia+"%")
	#print("Rapporto positivi/tamponi MOLECOLARI ultimo giorno = %.2f" %tassoNazionalePositiviMolecolari+"%")
	#print("Rapporto positivi/tamponi MOLECOLARI ultima settimana = %.2f" %tassoNazionalePositiviMolecolariUltimaSettimana+"%")
	#print("Ingressi terapia intensiva ultimo giorno = "+str(ingressiUltimoGiornoTerapiaIntensivaInItalia))
	#print("Ingressi terapia intensiva ultima settimana = "+str(nuoveTerapieIntensiveUltimaSettimanaItalia))
	#rint("Ingressi NON terapia intensiva ultimo giorno = "+str(ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia))
	#print("Ingressi NON terapia intensiva ultima settimana = "+str(ingressiUltimaSettimanaOspedaleSenzaTerapiaIntensivaInItalia))
	#print("Deceduti giornalieri = "+str(decedutiUltimoGiorno.sum()))
	#print("Deceduti settimanali = "+str(decedutiUltimaSettimana.sum()))
	#print("Letalita da inizio pandemia = %.2f" %tassoDiMortalitaNazionale+"%")


	regioni=covid19UltimoGiorno.index

	covid19Mappa=pd.DataFrame({"Regione":regioni,"Rapporto giornaliero su tamponi totali":rapportoPositiviSuTotaleTamponiUltimoGiorno,"Rapporto giornaliero su tamponi molecolari":tassoPositiviMolecolari,"Ingressi giornalieri in intensiva":ingressiUltimoGiornoTerapiaIntensiva,"Ingressi giornalieri fuori dall'intensiva":ingressiUltimoGiornoOspedaleSenzaTerapiaIntensiva,"Deceduti giornalieri":decedutiUltimoGiorno,"Rapporto settimanale su tamponi totali":rapportoPositiviUltimaSettimana,"Rapporto settimanale su tamponi molecolari":tassoPositiviMolecolariUltimaSettimana,"Ingressi settimanali in intensiva":nuoveTerapieIntensiveUltimaSettimana,"Ingressi settimanali fuori dall'intensiva":ingressiUltimaSettimanaOspedaleSenzaTerapiaIntensiva,"Deceduti settimanali":decedutiUltimaSettimana,"Letalita":tassoDiMortalita})

	#AGGIUNGIAMO LE COLONNE RELATIVE AL DATO NAZIONALE
	covid19Mappa["Rapporto Italiano su tamponi totali"]= [rapportoPositiviTamponiUltimoGiornoInItalia for i in range(21)]
	covid19Mappa["Rapporto Italiano su tamponi molecolari"] = [tassoNazionalePositiviMolecolari for i in range(21)]
	covid19Mappa["Ingressi in intensiva in Italia"]= [ingressiUltimoGiornoTerapiaIntensivaInItalia for i in range(21)]
	covid19Mappa["Ingressi in ospedale non intensiva in Italia"]= [ingressiUltimoGiornoOspedaleSenzaTerapiaIntensivaInItalia for i in range(21)]
	covid19Mappa["Deceduti in Italia"]= [decedutiUltimoGiorno.sum()  for i in range(21)]


	covid19Mappa["Rapporto Italiano su tamponi totali settimanali"]= [rapportoPositiviUltimaSettimanaInItalia for i in range(21)]
	covid19Mappa["Rapporto Italiano su tamponi molecolari settimanali"] = [tassoNazionalePositiviMolecolariUltimaSettimana for i in range(21)]
	covid19Mappa["Ingressi in intensiva in Italia settimanali"]= [nuoveTerapieIntensiveUltimaSettimanaItalia for i in range(21)]
	covid19Mappa["Ingressi in ospedale non intensiva in Italia settimanali"]= [ingressiUltimaSettimanaOspedaleSenzaTerapiaIntensivaInItalia for i in range(21)]
	covid19Mappa["Deceduti in Italia settimanali"]= [decedutiUltimaSettimana.sum()  for i in range(21)]

	covid19Mappa["Tasso di mortalita nazionale"]= [tassoDiMortalitaNazionale for i in range(21) ]

	if os.path.exists("csv/Covid19PerFareLeMappe.csv"):
		os.remove("csv/Covid19PerFareLeMappe.csv")

	covid19Mappa.to_csv("csv/Covid19PerFareLeMappe.csv",index=False)

