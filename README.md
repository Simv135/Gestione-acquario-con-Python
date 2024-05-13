# Gestione acquario con Python
 Applicazione che permette la gestione automatica dei parametri principali di un acquario (illuminazione e temperatura) mediante comunicazione seriale con microcontrollore (ad esempio Arduino).
 
 ![GUI](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/5013f7c2-8518-48df-956f-36dd1349c51f)

# Installazione
 Il programma, realizzato in *Python 3.12.1* (o superiori), è in grado di funzionare su qualunque sistema operativo che possieda e supporti tale versione.
 
 Dopo l'installazione della corrente versione di Python dal [sito ufficiale](https://www.python.org/downloads/) aprire il terminale (o prompt dei comandi) del proprio sistema operativo e digitare i seguenti 
comandi, accettando le procedure di installazione:
  + ***pip install tkinter***
  + ***pip install time***
  + ***pip install serial***
  + ***pip install webbrowser***

 Se dovesse verificarsi questo errore la libreria è già installata:
  > ERROR: Could not find a version that satisfies the requirement tkinter (from versions: none)
  > 
  > ERROR: No matching distribution found for tkinter
 
 Il file *"gestione_acquario_v1.py"* è pronto per essere aperto con Python!
 
# Modalità d'uso
 L'applicazione si aprirà insieme ad un terminale che può essere utilizzato per osservare lo scambio di dati che avviene tra il computer e il microcontrollore. Esso non è fondamentale 
 per l'utilizzo del programma.
 
 Per la connessione è sufficiente selezionare la **porta COM** corrispondente alla connessione USB del nostro microcontrollore e selezionare la velocità di trasmissione dei dati (**Baud rate**) del microcontrollore.

 Se la connessione è avvenuta in modo corretto sarà possibile leggere la temperatura dell'acquario in gradi Celsius, proveniente dal sensore di temperatura connesso al microcontrollore.

 E' possibile controllare automaticamente la **temperatura** del nostro acquario: alla pressione del pulsante *"Termostato"* la temperatura rilevata dal sensore di temperatura sarà comparata con quella impostata manualmente dallo slider e verrà attivata o disattiva una piastra riscaldante al fine di regolare la temperatura dell'acquario.

 In caso di lettura errata da parte del sensore di temperatura la piastra rimarrà disattivata.

 L'**illuminazione** può essere gestita in due modi: **manuale** e **ciclo giorno-notte**

 + **Modalità manuale**: accensione o spegnimento delle luci tramite pulsante *"Illuminazione"* (0% o 100%) o regolazione con valori di luminosità intermedi (da 0% a 100%) tramite l'utilizzo dello slider.

 + **Modalità ciclo giorno-notte**: alla pressione del pulsante *"ciclo giorno-notte"* si attiva la regolazione automatica della luminosità in modo graduale per simulare l'alba o il tramonto all'interno 
 dell'acquario. E' possibile impostare la durata di alba e tramonto dal menu *"Orario"* seguendo la sintassi *"hh:mm - hh:mm"* che indica l'ora di inizio e l'ora di fine dell'evento.

 L'orario preso in considerazione per la regolazione automatica della luminosità sarà quello del nostro dispositivo.

 Nella sezione *"Info"* è disponibile il pulsante Github che riporta l'utente alla pagina web del progetto.

# Specifiche
 Velocità di trasmissione (Baud rate): 9600, 57600, 115200, 230400 (baud)
 Range di temperatura regolabile: 15 °C - 30 °C

 Dati in scrittura:
 0 - 255  --> Luminosità
 256 - 257 --> Piastra riscaldante OFF - ON

 Dati in lettura:
 1 °C - 31 °C --> Temperatura del sensore (i dati al di fuori di questo range non verranno presi in considerazione)
 
 
