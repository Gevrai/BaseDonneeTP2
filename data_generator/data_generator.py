from faker import Factory
import eventful
import random
import simplejson
from datetime import datetime

api = eventful.API('NGGMrssxfJT52ZSP')

# Create object factory with en_CA locale
fake = Factory.create('en_CA')
fake.seed('12345')

# Constants
nb_clients = 100
villes = ['Montreal','Ottawa','Toronto']
nb_evenements_par_ville = 2

# Global variables
client_list = []
event_list = [] 
categ_list = []
empl_list = []
occurence_list = []
transaction_list = []
rabais_list = []

#Counters

class Client():
    def __init__(self, id):
        global fake
        self.clientID = id
        self.nom=fake.last_name()
        self.prenom = fake.first_name()
        self.couriel = fake.free_email()
        self.password = fake.password(length=10)
        self.numCivique = fake.building_number()
        self.rue = fake.street_name()
        self.codePostal = fake.postalcode()
        self.ville = fake.city()
        self.province = fake.province_abbr()
        self.numTel = fake.phone_number()

class Evenement():
    def __init__(self, e, id):
        self.evenementID = id
        self.titre = e['title']
        self.description = e['description']
        self.siteWeb = e['url']
        self.duree = random.choice([1,1.5,2,2.5,3,4,6,10,24,48])
        global categ_list
        for c in categ_list:
            if (c.APIname == e['categories']['category'][0]['name']):
                self.categorie = c
                return
        print "ERROR:Categorie " + e['categories']['category'][0]['name'] +" inexistante" 

class Categorie():
    def __init__(self, cat):
        self.APIname = cat
        cat = cat.replace('&amp;','and').split(': ',1)
        if(len(cat) == 2):
            self.surCategorie = cat[0]
            self.categorie = cat[1]
        else: 
            self.categorie = cat[0]
            self.surCategorie = None

class Occurence():
    def __init__(self, id, evenementID, emplacementID, start_time=None, prix = None):
        global fake
        self.occurenceID = id
        if (start_time == None):
            '''2003-01-01 2:00:00'''
            self.dateEtHeure = fake.date_time_between_dates(datetime(2016,01,01),datetime(2020,12,30)).isoformat(' ')
        else:
            self.dateEtHeure = start_time
        self.prix = '%.2f' % random.uniform(5.0,75.0)
        self.evenementID = evenementID
        self.emplacementID = emplacementID

class Emplacement():
    def __init__(self, e, id):
        global fake
        self.emplacementID = id
        self.siteID = e['id'] 
        self.nom = e['venue_name']
        self.siteWeb = e['url']
        self.capacite = random.choice([50,100,200,300,500,1000,2000,5000,10000,15000])
        if (e['address'] != None):
            address = e['address'].split(' ',1)
            self.numCivique = address[0]
            if (len(address) == 2):
                self.rue = address[1]
            self.codePostal = e['postal_code']
            self.ville = e['city_name']
            self.province = e['region_abbr']
        else:
            address = None
            self.numCivique = None
            self.rue = None
            self.codePostal = None
            self.ville = None
            self.province = None

        self.numTel = fake.phone_number()

class Transaction():
    def __init__(self, transactionID, clientID, occurenceID, prix, codeRabais=None):
        global fake
        self.transactionID = transactionID 
        self.clientID = clientID
        self.occurenceID = occurenceID
        self.statut = random.choice(["en attente","payee","approuvee","annulee"])
        self.codeRabais = codeRabais
        if (codeRabais == None):
            self.cout = prix 
        else:
            tauxRabais = 1.0
            for c in rabais_list:
                if (c.code == codeRabais):
                    tauxRabais = c.tauxRabais
            self.cout = prix*tauxRabais
        self.dateEtHeure = fake.date_time_between_dates(datetime(2016,01,01),datetime(2020,12,30)).isoformat(' ')
        self.modePaiement = random.choice(['mastercard','visa','debit','paypal'])

class Rabais():
    def __init__(self, code): 
        global fake
        self.code = code
        self.tauxRabais = random.choice([0,.5,.6,.7,.8,.85,.9,.95])
        self.expiration = fake.date_time_between_dates(datetime(2016,01,01),datetime(2020,12,30)).date().isoformat()

def fetchEventsVenues(page=1):
    # Remplissage d'evenements et de leur emplacement en meme temps
    events = simplejson.load(open('json/event_page'+str(page)+'.json', 'r'))
    global event_list 
    global empl_list
    for event in events['events']['event']:
        print 'Events: ' + str(len(event_list)) + '/2250    Emplacements: ' + str(len(empl_list)) 
        e = Evenement(event, len(event_list))
        if (not contientVenueID(event, empl_list)):
            v = fetchVenueByID(event['venue_id'], len(empl_list))
            empl_list.append(v)
        emplID = fetchVenueID(event['venue_id'])
        o = Occurence(
                id=len(event_list),
                evenementID=len(empl_list),
                emplacementID = emplID,
                start_time=event['start_time'],
                prix=event['price'])
        event_list.append(e)
        occurence_list.append(o)

def contientVenueID(e,empl_list):
    for empl in empl_list:
        if empl.siteID == e['venue_id']:
            return True
    return False

def fetchVenueID(siteID):
    for empl in empl_list:
        if empl.siteID == siteID:
            return empl.emplacementID

def fetchVenueByID(venueid, id):
    empl = api.call('venues/search', l= venueid) 
    return Emplacement(empl['venues']['venue'],id)

def createRandomOccurrence():
    global event_list 
    global empl_list 
    global occurence_list
    even = random.choice(event_list)
    empl = random.choice(empl_list)
    occu = Occurence(
            id=len(occurence_list),
            evenementID = even.evenementID,
            emplacementID = empl.emplacementID,
            start_time = fake.date_time_between_dates(datetime(2016,01,01),datetime(2020,12,30)).isoformat(' '))
    occurence_list.append(occu)

def createRabais():
    global rabais_list
    for i in range(6):
        rabais_list.append(Rabais(i+1))

def createRandomTransaction():
    global event_list 
    global empl_list 
    global occurence_list
    global transaction_list

    if (random.random() > 0.75):
        codeRabais = random.randint(1,6)
    c = random.choice(client_list)
    o = random.choice(occurence_list)
    t = Transaction(
            transactionID = len(transaction_list),
            clientID = c.clientID,
            occurenceID = o.occurenceID,
            prix = o.prix,
            codeRabais=None)
    transaction_list.append(t)


# Remplissage de clients
for id in range(nb_clients):
    client_list.append(Client(id))

# Remplissage de categories a partir du fichier 'categories.json'
categories = simplejson.load(open('json/categories.json', 'r'))
for categ in categories['category']:
    c = Categorie(categ['name'])
    categ_list.append(c)
    print c.categorie
   
for page in range(1,10):
    fetchEventsVenues(page)
print "Evenements: " + str(len(event_list))
print "Emplacements:  " + str(len(empl_list)) 

for i in range(1000):
    createRandomOccurrence()
print "Occurrences: " + str(len(occurence_list))

createRabais()
print "Rabais: " + str(len(rabais_list))

for i in range(1000):
    createRandomTransaction()
print "Transactions: " + str(len(transaction_list))

