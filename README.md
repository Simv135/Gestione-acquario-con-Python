# Gestione acquario con Python
 Applicazione per la gestione automatica dei principali parametri di un acquario mediante comunicazione seriale (USB) con un qualsiasi microcontrollore che supporti tale modalità di comunicazione (ad esempio Arduino).
 
 ![GUI](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/5013f7c2-8518-48df-956f-36dd1349c51f)

# Installazione
 Il programma, realizzato in *Python 3.12.1* (o superiori), è in grado di funzionare su qualunque sistema operativo che possieda e supporti tale versione.
 
 Dopo l'installazione della corrente versione di Python dal [sito ufficiale](https://www.python.org/downloads/) aprire il terminale (o prompt dei comandi) del proprio sistema operativo e digitare i seguenti 
comandi, accettando le procedure di installazione:
  + `pip install tkinter`
  + `pip install time`
  + `pip install serial`
  + `pip install webbrowser`
 
 Se dovesse verificarsi questo errore la libreria è già installata:
  > ERROR: Could not find a version that satisfies the requirement tkinter (from versions: none)
  > 
  > ERROR: No matching distribution found for tkinter
 
 Il file *"gestione_acquario_v1.py"* è pronto per essere aperto con Python!
 
# Modalità d'uso
 Per la connessione è sufficiente selezionare la **porta COM** corrispondente alla connessione USB del nostro microcontrollore e selezionare la velocità di trasmissione dei dati (**Baud rate**) del microcontrollore.

![PortMENU](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/a58586ba-6dff-4b94-979a-2ebaf0cb5ce1)

![BaudMENU](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/9bfc9bcb-a000-411b-9653-d2295b1ddec7)

 Se la connessione è avvenuta in modo corretto sarà possibile leggere la temperatura dell'acquario in gradi Celsius, proveniente dal sensore di temperatura connesso al microcontrollore.

![Temp](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/4ef568e8-65f8-426a-83be-68ab85f73cd7)

 E' possibile controllare automaticamente la **temperatura** del nostro acquario: alla pressione del pulsante *"Termostato"* la temperatura rilevata dal sensore di temperatura sarà comparata con quella impostata manualmente dallo slider e verrà attivata o disattiva automaticamente una piastra riscaldante al fine di regolare la temperatura all'interno dell'acquario.

![TempSLIDER](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/c151843f-c61c-47c5-b1ed-04f97ee7f9bc)

 In caso di lettura errata da parte del sensore di temperatura la piastra rimarrà disattivata.

![DATATinvalid](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/36507ac1-78b9-420c-b431-9a397188663d)

 L'**illuminazione** può essere gestita in due modi: **manuale** e **ciclo giorno-notte**

 + **Modalità manuale**: accensione o spegnimento delle luci tramite pulsante *"Illuminazione"* (0% o 100%) o regolazione con valori di luminosità intermedi (da 0% a 100%) tramite l'utilizzo dello slider.

![LuxSLIDER](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/d6c436df-b270-4d1c-a11d-4f4854e0f70b)

 + **Modalità ciclo giorno-notte**: alla pressione del pulsante *"ciclo giorno-notte"* si attiva la regolazione automatica della luminosità in modo graduale per simulare l'alba o il tramonto all'interno 
 dell'acquario. E' possibile impostare la durata di alba e tramonto dal menu *"Orario"* seguendo la sintassi *"hh:mm - hh:mm"* che indica l'ora di inizio e l'ora di fine dell'evento.

![OrarioMENU](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/4e0db3a3-a1fe-419a-a699-0e9052f6d0df)

 L'orario preso in considerazione per la regolazione automatica della luminosità sarà quello del nostro dispositivo.

 L'applicazione si aprirà insieme ad un terminale che può essere utilizzato per osservare lo scambio di dati che avviene tra il computer e il microcontrollore. Esso non è fondamentale 
 per l'utilizzo del programma ma è necessario tenerlo aperto.

 ![DATA](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/19354984-7024-4a4d-bddf-4498dec26409)

 All'interno del menu *"Info"* è disponibile la sezione *"Github"* che riporta l'utente alla pagina web del progetto.

 ![InfoMENU](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/7ed1e28f-340c-4d13-bbd6-943ea943f861)

# Specifiche
 Velocità di trasmissione (Baud rate): *9600*, *57600*, *115200*, *230400* (baud)

 Range di temperatura regolabile: *15 °C - 30 °C*

 **Dati in scrittura**:
 
 + *0 - 255*   --> Luminosità (0% - 100%)
 + *256 - 257* --> Piastra riscaldante (OFF - ON)

 **Dati in lettura**:
 
 + *1 - 31*    --> Temperatura del sensore (°C), i dati al di fuori di questo range non verranno presi in considerazione

# Il codice

Il codice del programma è basato su alcune librerie che è necessario importare (procedura di [installazione](#Installazione))

La libreria *"tkinter"* è fondamentale per la creazione dell'interfaccia utente, mentre *"serial"* permette lo scambio di dati tramite comunicazione seriale.

![code1](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/57b0946f-7470-46d2-aff9-9de032e70591)

Per la creazione di una nuova finestra è necessaria la creazione di una classe, a cui potranno fare riferimento le relative funzioni

![code2](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/808d9619-1446-428e-b001-7343a924e98b)

Si definiscono alcune informazioni della finestra come titolo, dimensioni ed il comportamento degli elementi all'interno della finestra

![code3](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/6fde139c-61fb-44b7-9be0-d88914859e7d)

Le principali variabili come la temperatura da mantenere, la luminosità impostata e gli orari di alba e tramonto per l'illuminazione

![code4](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/ec2b4123-81c0-43a8-9eb9-83f2b0e8cfea)

La creazione dei menu in cascata e dei suoi elementi, ciascuno dei quali richiama una funzione (menu *Info* nell'esempio sottostante)

![code5](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/ee10d6bd-44ae-4d14-9345-7c05f317b213)

In seguito il menu in cascata per il baud rate: per ogni elemento della lista *"baud_rates"* viene aggiunto un elemento al menu in cascata con un comando corrispondente da fornire alla funzione *"set_baud_rate()"* per selezionare il valore desiderato all'interno del menu

![code6](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/efc56952-e941-42c8-b32f-235c16335191)

Esempio di un pulsante che richiama la propria funzione quando premuto, viene definito il suo nome e la sua posizione nella finestra dell'app (pulsante *Illuminazione* nell'esempio sottostante)

![code7](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/9181c0b4-e937-44cc-b1c0-ee29b5a7f889)

Slider per il controllo dell'illuminazione: definizione dei suoi principali parametri (simili a quelli degli altri elementi) e della luminosità di default all'avvio dell'applicazione

![code8](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/d7c06945-aab0-42a9-8289-d4469913b890)

Inizializzazione della connessione seriale con il microcontrollore con porta e baud rate selezionati, attesa di 1 secondo affinchè avvenga la connessione ed invio dei dati al microcontrollore

![code9](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/512de9cf-8e74-45d5-a723-a831e34eeb34)

Quando viene richiamata la funzione *"connect()"* per la connessione seriale senza dei valori da inviare al microcontrollore e se l'argomento della funzione è *""* si entra in una fase di lettura in cui si attende la ricezione dei dati da parte del dispositivo connesso

![code10](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/2207f1d3-7c98-495d-997c-91b2a74fade3)

All'avvio dell'app o alla pressione di *"ALT + R"* vengono testate le connessioni con le porte COM fino alla numero 30, aggiornando di conseguenza il menu in cascata relativo ad esse. Le porte già presenti in lista non vengono nuovamente aggiunte.

![code11](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/dda71044-ed03-446b-9046-e74cd928f43d)

Invio dei valori di luminosità prelevati dalla posizione dello slider nello spazio, successivamente alla conversione da un valore di tipo percentuale 0%-100% ad un valore 0-255. Il valore di luminosità *"0"* comporta un cambio di colore del pulsante per indicare che le luci sono spente.

![code12](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/6d8da238-e46a-4fdf-b876-f31fe6f4559c)

Lettura automatica del valore di temperatura ogni 20 secondi. L'argomento della funzione *"self.connect("")"* è vuoto per indicare che nella funzione deve avvenire un'operazione di lettura, come indicato precedentemente.

![code13](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/7dbd4527-0546-4aa1-a67d-4af5a338c6f6)

Gli orari prelevati dalla finestra di dialogo inseriti come "ORA_INIZIO:MINUTO_INIZIO - ORA_FINE:MINUTO_FINE"
+ vengono suddivisi in una lista come *"ORA_INIZIO:MINUTO_INIZIO"* e *"ORA_FINE:MINUTO_FINE"*

![code15](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/83051718-7d9f-4887-9beb-6b050d1114d2)

+ e poi adattati come una somma di stringhe *"ORA_INIZIO + MINUTO_INIZIO"* (ad esempio *"19:00"* diventa *"1900"*)

![code16](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/3bc117c7-9f5b-4b03-8766-c87255c5ea3b)

Controllo dell'orario attuale per il confronto con l'orario preimpostato di alba e tramonto al fine di ottenere una regolazione proporzionale della luminosità:
+ *0 %*         --> in fase notturna
+ *0 % - 100 %* --> controllo proporzionale inizio - fine alba
+ *100 %*       --> in fase diurna
+ *100 % - 0 %* --> controllo proporzionale inizio - fine tramonto

![code14](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/b00dc8d8-153d-4cbf-b759-3d1fc18a35c9)

In questa descrizione sono state commentate solo alcune parti fondamentali del codice, è possibile leggere l'intero codice commentato aprendo il file del programma con un qualsiasi editor di testo.

# Esempio di interfacciamento con Arduino

+ Schema di montaggio
![schema_montaggio_arduino](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/3eb34f3d-02c0-4815-b357-825a4b9c0646)

+ Schema elettrico
![schema_Arduino](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/ee7b7512-9268-4d17-ba2a-429756385952)

+ Codice
![code_Arduino](https://github.com/Simv135/Gestione-acquario-con-Python/assets/109431365/57d92a21-729b-430b-a86e-207c5e831b58)
