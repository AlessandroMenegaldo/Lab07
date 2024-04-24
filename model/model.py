import copy

from database.meteo_dao import MeteoDao

from database import meteo_dao


class Model:
    def __init__(self):
        self.rilevazioni = []
        self.soluzione_sequenza = []
        self.costo_soluzione = 10000000000

    def  calcola_umidita_media(self, mese):
        self.rilevazioni = meteo_dao.MeteoDao.get_all_situazioni()
        umidita_media_genova = self.calcola_umidita_media_localita(mese, "Genova")
        umidita_media_torino = self.calcola_umidita_media_localita(mese, "Torino")
        umidita_media_milano = self.calcola_umidita_media_localita(mese, "Milano")
        return umidita_media_genova, umidita_media_torino, umidita_media_milano

    def calcola_umidita_media_localita(self, mese : int,localita):
        contatore=0
        somma=0

        for situazione in self.rilevazioni:
            if (situazione.localita == localita) and (situazione.data.month == int(mese)):
                somma += situazione.umidita
                contatore = contatore + 1

        if contatore!=0:
            return somma/contatore
        return "ERRORE RICERCA UMIDITÀ"


    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################

    def calcola_sequenza_citta_analisi(self,mese):
        self.rilevazioni=[] #reset
        self.costo_soluzione = 10000000000 #reset
        self.soluzione_sequenza = []

        self.rilevazioni = meteo_dao.MeteoDao.get_situation_by_month(mese)
        self._ricorsione([])

        return self.soluzione_sequenza, self.costo_soluzione


    def _ricorsione(self,parziale):

        #condizione terminale
        if len(parziale)==15:
            costo_parziale= self.calcola_costo_soluzione(parziale)
            if costo_parziale < self.costo_soluzione:
                self.costo_soluzione = costo_parziale
                self.soluzione_sequenza = copy.deepcopy(parziale)


        #caso ricorsivo
        else:
            for situazione in self.situazioni_domani(len(parziale)+1):

                parziale.append(situazione)
                if self.vincolo_giorni_rispettato(parziale):
                    self._ricorsione(parziale)
                parziale.pop()



    def situazioni_domani(self,domani):
        situa_domani=[]
        for situazione in self.rilevazioni:
            if situazione.data.day == domani:
                situa_domani.append(situazione)
        return situa_domani





    def vincolo_giorni_rispettato(self,parziale):
        """
        In nessuna città si possono trascorrere più di 6 giornate (anche non consecutive)
        Scelta una città, il tecnico non si può spostare prima di aver trascorso 3 giorni consecutivi.
        """
        milano=6
        torino=6
        genova=6
        citta_attuale=parziale[0].localita
        giorni_consecutivi=0
        for situazione in parziale:
            if situazione.localita=="Genova":
                genova -= 1
            if situazione.localita=="Torino":
                torino -= 1
            if situazione.localita=="Milano":
                milano -= 1

            if (milano < 0 or torino < 0 or genova < 0):
                return False

            #secondo vincolo
            if situazione.localita != citta_attuale: #se cambia citta
                if (giorni_consecutivi < 3): # ogni volta che cambio tranne la prima città
                    return False

                giorni_consecutivi = 0 #azzero contatore
                citta_attuale = situazione.localita #cambio la città attuale

            giorni_consecutivi +=1 #incremento giorni nella città attuale

        return True

    def calcola_costo_soluzione(self,parziale):
        """
        calcolo costo soluzione:
        Le analisi hanno un costo per ogni giornata, determinato dalla somma di due contributi:
        un fattore costante (di valore 100) ogniqualvolta il tecnico si deve spostare da una
        città ad un’altra in due giorni successivi, ed un fattore variabile pari al valore numerico
        dell’umidità della città nel giorno considerato.
        """
        costo=0
        giorno_attuale = parziale[0].localita
        for giorno in parziale:
            if giorno.localita != giorno_attuale:
                costo +=100
            costo+=giorno.umidita

        return costo








