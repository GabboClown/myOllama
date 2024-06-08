import requests
import json
import customtkinter as custk

class Finestra:
    def __init__(self, titolo):
        # Setup custom tkinter
        custk.set_appearance_mode("System")
        custk.set_default_color_theme("blue")

        # Setup della root
        self.__root = custk.CTk()
        self.__root.title(titolo)
        self.__root.geometry("720x720")

        self.prompt = custk.StringVar()

        self.listaBottoni = {}
        self.listaLabel = {}
        self.listaEntry = {}

    def start(self):
        self.__root.mainloop()

    def reset(self): # Pulisce la label di risposta
        if 'risposta' in list(self.listaLabel.keys()): self.listaLabel['risposta'].configure(text = '')

    def getRoot(self):
        return self.__root

class apiRequest:
    def __init__(self):
        self.__url = ''
        self.__headers = {}
        self.__data = {}
        self.__responded = False
        self.__response = requests.models.Response()

    def setURL(self, url):
        self.__url = url
    def setHeaders(self, headers):
        self.__headers = headers
    def setData(self, data):
        self.__data = data
    
    def getURL(self):
        return self.__url
    def getHeaders(self):
        return self.__headers
    def getJsonData(self):    # Restituisce il dump del campo data del pacchetto in formato JSON
        return json.dumps(self.__data)
    def getResponseObj(self): # Restituisce l'intero oggetto di risposta, se trovato
        if self.__responded:
            return self.__response
        else: raise TypeError("Non hai inviato alcuna richiesta")
    def getResponseTextJson(self): # Restituisce il testo della risposta sotto formato JSON
        if self.__responded: 
            return json.loads(self.__response.text)
        else: raise TypeError("Non hai inviato alcuna richiesta")
    
    def startRequest(self, prompt = None):
        if prompt != None: self.__data['prompt'] = prompt

        self.__response = requests.post(self.getURL(), headers = self.getHeaders(), data = self.getJsonData())
        self.__responded = True

# Wrapper delle istruzioni da eseguire quando l'utente preme il bottone "Invia"
def sendWrapper():
    myOllama.reset()
    request.startRequest(myOllama.prompt.get())
    if 'risposta' not in list(myOllama.listaLabel.keys()):
        myOllama.listaLabel['risposta'] = custk.CTkLabel(myOllama.getRoot(), text = f"Ecco la tua risposta:\n{request.getResponseTextJson()['response']}", font = custk.CTkFont('Roboto', 15), wraplength = 600)
        myOllama.listaLabel['risposta'].pack(pady = 10)
    else:
        myOllama.listaLabel['risposta'].configure(text = f"Ecco la tua risposta:\n{request.getResponseTextJson()['response']}")



if __name__ == "__main__":
    myOllama = Finestra("myOllama") # Oggetto della finestra da visualizzare
    request = apiRequest()          # Oggetto della richiesta da inviare

    request.setURL("http://localhost:11434/api/generate")
    request.setHeaders({'Content-Type' : 'application/json'})
    request.setData({'model' : 'phi3', 'prompt' : None, 'stream' : False})

    # Creazione label titolo
    myOllama.listaLabel['titolo'] = custk.CTkLabel(myOllama.getRoot(), text = "myOllama", font = custk.CTkFont('Roboto', 25, 'bold'))
    myOllama.listaLabel['titolo'].pack(pady = 10)

    # Creazione label sottotitolo
    myOllama.listaLabel['sottotitolo'] = custk.CTkLabel(myOllama.getRoot(), text = "Un client AI di Ollama che non sapevi di aver bisogno...", font = custk.CTkFont('Roboto', 17, slant = 'italic'))
    myOllama.listaLabel['sottotitolo'].pack()

    # Creazione label dove viene richiesto il prompt
    myOllama.listaLabel['richiesta'] = custk.CTkLabel(myOllama.getRoot(), text = "Inserisci il tuo prompt:", font = custk.CTkFont('Roboto', 15, slant = 'italic'))
    myOllama.listaLabel['richiesta'].pack(pady = 30)

    # Creazione entry field del prompt
    myOllama.listaEntry['prompt'] = custk.CTkEntry(myOllama.getRoot(), width = 350, height = 40, textvariable = myOllama.prompt)
    myOllama.listaEntry['prompt'].pack(pady = 10)

    # Creazione bottone d'invio
    myOllama.listaBottoni['invio'] = custk.CTkButton(myOllama.getRoot(), text = "Invia", command = sendWrapper)
    myOllama.listaBottoni['invio'].pack(pady = 10)

    # Creazione bottone della pulizia della label di risposta
    myOllama.listaBottoni['pulisci'] = custk.CTkButton(myOllama.getRoot(), text = "Pulisci", command = myOllama.reset)
    myOllama.listaBottoni['pulisci'].pack(pady = 10)

    myOllama.start()
