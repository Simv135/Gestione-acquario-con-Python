import tkinter as tk                            #importazione delle librerie necessarie
from tkinter import messagebox
import time, serial, webbrowser

class AcquarioApp(tk.Tk):
    def __init__(self):

        #FINESTRA PRINCIPALE
        super().__init__()
        self.title("Acquario")
        self.geometry("230x210")
        self.resizable(False, False)            #disattiva la capicità della finestra di cambiare di dimensione
        self.frame = tk.Frame(self)
        self.frame.pack(expand=True, fill=tk.BOTH)

        #########################################

        #VALORI DEFAULT ALL'AVVIO DELL'APP
        self.set_temperatura = 25               # (°)
        self.luminosita_attuale = 50            # (%)
        
        self.controllo_temperatura = False      #stato bottoni
        self.lampada_led_attiva = False         
        self.controllo_luminosita = False       
        
        self.alba_inizio = 600                  #orario alba 06:00 - 07:00
        self.alba_fine = 700
        
        self.tramonto_inizio = 1900             #orario tramonto 19:00 - 20:00
        self.tramonto_fine = 2000

        #########################################

        #BARRA DEI MENU
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        #MENU ALBA-TRAMONTO
        self.orari_menu = tk.Menu(self.menu_bar, tearoff=0)      #casella per selezionare manualmente gli orari di alba e tramonto
        self.menu_bar.add_cascade(label="Orario", menu=self.orari_menu)
        self.orari_menu.add_command(label=f"Alba (06:00 - 07:00)", command=self.modifica_orario_alba)
        self.orari_menu.add_command(label=f"Tramonto (19:00 - 20:00)", command=self.modifica_orario_tramonto)

        #MENU PORTE COM
        self.port=""
        self.baud_rate=9600
        self.port_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Porta", menu=self.port_menu)
        self.port_menu_commands = []                             #crea lista vuota del menu sulle porte COM (che sarà successivamente riempita con le porte attive)
        self.bind('<Alt-r>', self.com_update)                    #tasto rapido aggiornamento delle porte COM
        
        #MENU BAUD RATE
        self.baud_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Baud rate", menu=self.baud_menu)
        self.baud_rates = [9600, 57600, 115200, 230400]          #lista baud rate di comunicazione più comuni con Arduino
        for baud_rate in self.baud_rates:                        #crea il menu in cascata dei baud rate selezionando quelli della lista
            self.baud_menu.add_command(label=str(baud_rate), command=lambda b=baud_rate: self.set_baud_rate(b))
        self.baud_menu.entryconfig(0, foreground="green")        #seleziona di default 9600 baud

        #MENU INFO
        self.info_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Info", menu=self.info_menu)
        self.info_menu.add_command(label="Github", command=self.website)    #apertura sito web del progetto
        
        #########################################

        #TEMPERATURA (RILEVATA)
        self.temp = tk.StringVar()                                                       #creazione stringa per la visualizzazione della temperatura
        self.temp.set("Temperatura attuale: - °C")          
        self.temperatura_label = tk.Label(self.frame, textvariable=self.temp)
        self.temperatura_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        #TEMPERATURA (CONTROLLO)
        self.termostato_button = tk.Button(self.frame, text="Termostato", command=self.termostato, fg="red")
        self.termostato_button.grid(row=1, column=0, padx=5, pady=5)                     #pulsante ON/OFF termostato
        
        self.temperatura_slider = tk.Scale(self.frame, from_=15, to=30, orient=tk.HORIZONTAL, label="Temperatura (°C)", command=self.temperatura)
        self.temperatura_slider.set(self.set_temperatura)                                #selezione della temperatura da mantenere costante
        self.temperatura_slider.grid(row=1, column=1, padx=5, pady=5)

        #LUMINOSITA' (CONTROLLO)
        self.led_button = tk.Button(self.frame, text="Illuminazione", command=self.led, fg="red")
        self.led_button.grid(row=2, column=0, padx=5, pady=5)                            #pulsante ON/OFF illuminazione
        
        self.luminosita_slider = tk.Scale(self.frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Luminosità (%)", command=self.update_luminosita)
        self.luminosita_slider.set(self.luminosita_attuale)                              #selezione della luminosità
        self.luminosita_slider.grid(row=2, column=1, padx=5, pady=5)

        self.auto_control_button = tk.Button(self.frame, text="Ciclo giorno-notte", command=self.ciclo_giorno_notte, fg="red")
        self.auto_control_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)     #pulsante ON/OFF ciclo giorno-notte

        #########################################

        self.com_update()           #scansiona le porte COM per rilevare quelle attive

        self.luminosita()           #aggiornamento della luminosità secondo il ciclo giorno-notte
        
        self.update_temperatura()   #lettura della temperatura

        #########################################

    #CONNESSIONE INVIO/RICEZIONE DATI
    def connect(self, data):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)  #connessione alla porta COM selezionata, con il baud rate selezionato
                                                                            #attesa di 1 sec per la connessione
            self.ser.write(data.encode())                                   #invio dei dati richiamati dalla funzione
            
            if data=="":
                self.temperatura = self.ser.readline().decode().strip()
                if self.temperatura:                                        
                    print(self.port+" "+str(self.baud_rate)+" < "+self.temperatura)
                    if 1<int(self.temperatura)<31:                          #se i dati letti sono nel range aggiorna la visualizzazione della temperatura con questi dati                  
                        self.temp.set(f"Temperatura attuale: {self.temperatura} °C")
                    else:
                        self.temp.set(f"Temperatura attuale: - °C")                                              
        except:
            self.ser.close()                                                      #prova a connettersi altrimenti non fa nulla

    #AGGIORNA IL MENU SULLE PORTE SERIALI, MOSTRANDO SOLO LE PORTE APERTE ALLA COMUNICAZIONE
    def com_update(self, event=None):
        self.port_menu_commands.clear()     #cancella le porte precedenti per aggiornare con le nuove disponibili
        self.port_menu.delete(0, "end")

        for n_port in range(30):            #test porte da COM0 a COM30
            port = f"COM{n_port}"
            try:
                self.ser = serial.Serial(port, self.baud_rate)  #testa la connessione su ciascuna porta
                self.ser.close()
                if port not in self.port_menu_commands:         #se la connessione va a buon fine aggiungi la porta al menu
                    self.port_menu.add_command(label=port, command=lambda p=port: self.change_port(p))  #aggiungi il comando per cambiare porta su ogni elemento inserito nel menu
                    self.port_menu_commands.append(port)
            except:
                pass                                            #se la connessione non va buon fine non aggiunge la porta al menu

        if self.port_menu_commands:                             #se ci sono elementi nella lista delle porte seleziona di default la prima porta disponibile
            self.change_port(self.port_menu_commands[0])

    #SELEZIONE PORTA COM
    def change_port(self, port):
        try:
            self.port = port
            
            for n in range(len(self.port_menu_commands)):               #colora di nero le scritte di tutte le porte del menu
                self.port_menu.entryconfigure(n, foreground='black')
            self.port_menu.entryconfigure(self.port_menu_commands.index(port), foreground='green')  #colora di verde la porta selezionata
            
            self.ser = serial.Serial(port, self.baud_rate)  #testa la connessione alla porta selezionata
            self.ser.close()
            
        except:
            self.com_update()   #se la porta selezionata non è più disponibile aggiorna il menu delle porte COM per trovare quelle disponibili
        
        print(self.port+" "+str(self.baud_rate))
        self.connect("")                            

    #SELEZIONE BAUD RATE
    def set_baud_rate(self, baud_rate):
        for n in range(len(self.baud_rates)):   #colora di nero le scritte di tutti i valori di baud rate nel menu
            self.baud_menu.entryconfigure(n, foreground='black')
        self.baud_rate = baud_rate
        self.baud_menu.entryconfigure(self.baud_rates.index(self.baud_rate), foreground='green')  #colora di verde il valore selezionato
        print(self.port+" "+str(self.baud_rate))

        #########################################

    #AGGIORNAMENTO SLIDER LUMINOSITA'
    def update_luminosita(self, valore):    
        try:
            self.luminosita_attuale = int(valore)
            self.luminosita_slider.set(int(valore))     #quando il valore sullo slider viene modificato viene assegnato un nuovo valore di luminosità
            if int(valore) > 0:
                self.led_button.config(text="Illuminazione", fg="green")
            else:
                self.led_button.config(text="Illuminazione", fg="red")
            data=str(int(self.luminosita_attuale/100*255))      #conversione da 0-100 a 0-255 per adattarlo meglio alla scheda arduino
            print(self.port+" "+str(self.baud_rate)+" > "+data)
            self.connect(data)      #il nuovo valore di luminosità viene inviato tramite seriale
        except:
            messagebox.showerror("Errore", "Valore non valido!")

    #STATO TERMOSTATO
    def termostato(self):
        self.controllo_temperatura = not self.controllo_temperatura
        if self.controllo_temperatura:
            self.stato_termostato=True  
            self.termostato_button.config(text="Termostato", fg="green")
        else:
            self.stato_termostato=False              
            self.termostato_button.config(text="Termostato", fg="red")
        self.update_termostato()

    #ACCENSIONE/SPEGNIMENTO LUCI
    def led(self):
        if self.luminosita_attuale>0:        #aggiornamento slider secondo il pulsante di illuminazione
            self.led_button.config(text="Illuminazione", fg="red")
            self.update_luminosita(0)   
        else:
            self.led_button.config(text="Illuminazione", fg="green")
            self.update_luminosita(100)
    
    #TEMPERATURA VALORE SLIDER
    def temperatura(self, valore):
        self.set_temperatura = int(valore)
    
    #AGGIORNAMENTO DAL SENSORE DI TEMPERATURA
    def update_temperatura(self):
        self.connect("")
        self.after(10000, self.update_temperatura)  #controllo ogni 10 secondi

    #AGGIORNAMENTO STATO PIASTRA RISCALDANTE
    def update_termostato(self):
        if self.stato_termostato==False:
            self.connect("256")                                     #dato corrispondente allo spegnimento della piastra
            print(self.port+" "+str(self.baud_rate)+" > 256")
        if self.stato_termostato==True:
            try:
                if self.temperatura<self.set_temperatura:
                    self.connect("257")                             #dato corrispondente all'accensione della piastra
                    print(self.port+" "+str(self.baud_rate)+" > 257")
                if self.temperatura>self.set_temperatura:
                    self.connect("256")                             #dato corrispondente allo spegnimento della piastra
                    print(self.port+" "+str(self.baud_rate)+" > 256")
            except:
                self.connect("256")
                print(self.port+" "+str(self.baud_rate)+" > 256 (invalid temperature value)")
                
            self.after(20000, self.update_termostato)               #invia il dato dello stato della piastra ogni 20 secondi 

    #CONTROLLO LUMINOSITA' SECONDO L'ORARIO IMPOSTATO DI ALBA E TRAMONTO
    def luminosita(self):
        ora_attuale = int(time.strftime("%H%M", time.localtime()))      #controllo ora attuale per la regolazione della luminosità
        if self.controllo_luminosita:
            luminosita_=0
            if self.alba_inizio <= ora_attuale <= self.alba_fine:       #calcolo della luminosità proporzionale all'orario preimpostato
                luminosita_ = (ora_attuale - self.alba_inizio) * 100 / (self.alba_fine - self.alba_inizio)
            elif self.tramonto_inizio <= ora_attuale <= self.tramonto_fine:
                luminosita_ = 100 - ((ora_attuale - self.tramonto_inizio) * 100 / (self.tramonto_fine - self.tramonto_inizio))
            elif self.alba_fine <= ora_attuale <= self.tramonto_inizio:
                luminosita_ = 100
            else:
                luminosita_ = 0
            self.update_luminosita(luminosita_)     #aggiorna il valore di luminosità
        self.after(20000, self.luminosita)          #attendi 20 secondi prima di aggiornare la luminosità e inviare il nuovo valore

    #ATTIVA/DISATTIVA IL CONTROLLO AUTOMATICO DELLA LUMINOSITA' SECONDO IL CICLO GIORNO-NOTTE
    def ciclo_giorno_notte(self):
        self.controllo_luminosita = not self.controllo_luminosita
        if self.controllo_luminosita:
            self.auto_control_button.config(text="Ciclo giorno-notte", fg="green")
        else:
            self.auto_control_button.config(text="Ciclo giorno-notte", fg="red")

    #MENU ORARIO ALBA
    def modifica_orario_alba(self):
        dialog = OrarioFinestra(self, "Modifica orario alba", "hh:mm - hh:mm")  #apre la finestra di dialogo OrarioFinestra per l'alba
        self.wait_window(dialog)    #attende l'azione dell'utente e del valore di orario inserito
        if dialog.result:
            orari = dialog.result.split(" - ")  #suddivide dalla stringa l'orario iniziale da quello finale
            if len(orari) == 2:
                try:
                    ora_inizio = int(orari[0].replace(":", "")) #intende gli orari senza divisione ore-minuti per semplificare i calcoli
                    ora_fine = int(orari[1].replace(":", ""))

                    if ora_fine < ora_inizio:
                        ora_fine += 24 #l'ora finale non può essere minore di quella iniziale quindi si considera l'ora come del giorno dopo, sommando 24 ore

                    self.alba_inizio = ora_inizio
                    self.alba_fine = ora_fine
                    self.orari_menu.entryconfig(0, label=f"Alba ({dialog.result})") #aggiorna l'orario inserito mostrato nel menu in cascata
                except:
                    messagebox.showerror("Errore", "Inserisci un formato orario valido!")   #se si verifica un errore con i valori inseriti viene mostrato un avviso
            else:
                messagebox.showerror("Errore", "Inserisci un formato orario valido!")

    #MENU ORARIO TRAMONTO
    def modifica_orario_tramonto(self):
        dialog = OrarioFinestra(self, "Modifica orario tramonto", "hh:mm - hh:mm")  #apre la finestra di dialogo OrarioFinestra per il tramonto
        self.wait_window(dialog)    #attende l'azione dell'utente e del valore di orario inserito
        if dialog.result:
            orari = dialog.result.split(" - ")  #suddivide  dalla stringa l'orario iniziale da quello finale
            if len(orari) == 2:
                try:
                    ora_inizio = int(orari[0].replace(":", "")) #intende gli orari senza divisione ore-minuti per semplificare i calcoli
                    ora_fine = int(orari[1].replace(":", ""))

                    if ora_fine < ora_inizio:
                        ora_fine += 24 #l'ora finale non può essere minore di quella iniziale quindi si considera l'ora come del giorno dopo, sommando 24 ore

                    self.tramonto_inizio = ora_inizio
                    self.tramonto_fine = ora_fine
                    self.orari_menu.entryconfig(0, label=f"Tramonto ({dialog.result})") #aggiorna l'orario inserito mostrato nel menu in cascata
                except:
                    messagebox.showerror("Errore", "Inserisci un formato orario valido!")   #se si verifica un errore con i valori inseriti viene mostrato un avviso
            else:
                messagebox.showerror("Errore", "Inserisci un formato orario valido!")

    #APERTURA SITO WEB
    def website(self):
        webbrowser.open('https://github.com/Simv135/Gestione-acquario-con-Python')

#FINESTRA DI DIALOGO PER MODIFICARE L'ORARIO DELLE LUCI
class OrarioFinestra(tk.Toplevel):
    def __init__(self, parent, titolo, messaggio):
        super().__init__(parent)
        self.title(titolo)
        self.geometry("180x100")    #risoluzione della finestra di dialogo
        self.transient(parent)

        self.label = tk.Label(self, text=messaggio)
        self.label.pack(pady=5)

        self.orario_entry = tk.Entry(self)
        self.orario_entry.pack(pady=5)

        self.ok_button = tk.Button(self, text="OK", command=self.conferma)
        self.ok_button.pack(side=tk.LEFT, padx=10)

        self.cancel_button = tk.Button(self, text="Annulla", command=self.destroy)  #chiude la finestra di dialogo
        self.cancel_button.pack(side=tk.RIGHT, padx=10)

        self.result = None

    def conferma(self):     #salva il valore del nuovo orario
        self.result = self.orario_entry.get()
        self.destroy()      #chiude la finestra di dialogo

if __name__ == "__main__":
    app = AcquarioApp()
    app.mainloop()
