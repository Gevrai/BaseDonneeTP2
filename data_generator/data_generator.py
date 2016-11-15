#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import *
from faker import Factory
import eventful
import random
import simplejson

# Dirty encoding trick...
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Api key
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

def general_INSERT_str(tableName, columnNames, values):
    assert(len(columnNames) == len(values)),"Error inserting into '{}':\nColumn (size {}):\t{}\nValues (size {}):\t{}".format(
            tableName, str(len(columnNames)), str(columnNames), str(len(values)), str(values)) 
    assert(columnNames),"Nothing to INSERT into '{}' table!".format(tableName)
    # Making sure every element is a string with correct format
    cols_str, vals_str = ([],[])
    for e in columnNames:
        cols_str.append(str(e))
    for e in values:
        if (e == 'None' or not e):
            vals_str.append("NULL")
        elif (isinstance(e, basestring)):
            vals_str.append('"{}"'.format(e))
        else:
            vals_str.append(str(e))

    return "INSERT INTO {}\n({})\nVALUES\n({});".format(
            tableName, ', '.join(cols_str), ', '.join(vals_str))

class Client():
    def __init__(self, id):
        global fake
        self.clientID = id
        self.nom = fake.last_name()
        self.prenom = fake.first_name()
        self.couriel = fake.free_email()
        self.password = fake.password(length=10)
        self.numCivique = fake.building_number()
        self.rue = fake.street_name()
        self.codePostal = fake.postalcode()
        self.ville = fake.city()
        self.province = fake.province_abbr()
        self.numTel = fake.phone_number()

    def INSERT_str(self, tableName):
        columnNames = ['clientID','nom','prenom','couriel','password','numCivique','rue','codePostal','ville','province','numTel']
        values = [self.clientID,self.nom,self.prenom,self.couriel,self.password,self.numCivique,self.rue,self.codePostal,self.ville,self.province,self.numTel]
        return general_INSERT_str(tableName, columnNames, values)
        
# TODO SQL Interval syntax for 'duree'
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
                self.categorie = c.categorie
                return
        assert(true), "Categorie '{}' inexistante".format(e['categories']['category'][0]['name']) 

    def INSERT_str(self, tableName):
        columnNames = ['evenementID', 'titre', 'description', 'siteWeb', 'duree']
        values = [self.evenementID, self.titre, self.description, self.siteWeb, self.duree] 
        return general_INSERT_str(tableName, columnNames, values)

# TODO nom de categorie meme que le nom de la table, pas bon!
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

    def INSERT_str(self, tableName):
        columnNames = ['surCategorie', 'categorie']
        values = [self.surCategorie, self.categorie] 
        return general_INSERT_str(tableName, columnNames, values)

class Occurence():
    def __init__(self, id, evenementID, emplacementID, start_time=None, prix = None):
        global fake
        self.occurenceID = id
        if (start_time == None):
            '''2003-01-01 2:00:00'''
            self.dateEtHeure = fake.date_time_between_dates(datetime(2016,01,01),datetime(2020,12,30)).isoformat(' ')
        else:
            self.dateEtHeure = start_time
        self.prix = float2decimal(random.uniform(5.0,75.0))
        self.evenementID = evenementID
        self.emplacementID = emplacementID

    def INSERT_str(self, tableName):
        columnNames = ['occurenceID', 'dateEtHeure', 'prix', 'evenementID', 'emplacementID']
        values = [self.occurenceID, self.dateEtHeure, self.prix, self.evenementID, self.emplacementID] 
        return general_INSERT_str(tableName, columnNames, values)

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

    def INSERT_str(self, tableName):
        columnNames = ['emplacementID', 'siteID', 'nom', 'siteWeb', 'capacite', 'numCivique', 'rue', 'codePostal', 'ville', 'province', 'numTel']
        values = [self.emplacementID, self.siteID, self.nom, self.siteWeb, self.capacite, self.numCivique, self.rue, self.codePostal, self.ville, self.province, self.numTel] 
        return general_INSERT_str(tableName, columnNames, values)

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

    def INSERT_str(self, tableName):
        columnNames = ['transactionID', 'clientID', 'occurenceID', 'statut', 'codeRabais', 'cout', 'dateEtHeure', 'modePaiement']
        values = [self.transactionID, self.clientID, self.occurenceID, self.statut, self.codeRabais, self.cout, self.dateEtHeure, self.modePaiement] 
        return general_INSERT_str(tableName, columnNames, values)

class Rabais():
    def __init__(self, code):
        global fake
        self.code = code
        self.tauxRabais = random.choice([0,.5,.6,.7,.8,.85,.9,.95])
        self.expiration = fake.date_time_between_dates(datetime(2016,01,01),datetime(2020,12,30)).date().isoformat()

    def INSERT_str(self, tableName):
        columnNames = ['code', 'tauxRabais', 'expiration']
        values = [self.code, self.tauxRabais, self.expiration] 
        return general_INSERT_str(tableName, columnNames, values)

def fetchEventsVenues(page=1):
    # Remplissage d'evenements et de leur emplacement en meme temps
    events = simplejson.load(open('json/event_page'+str(page)+'.json', 'r'))
    global event_list
    global empl_list
    for event in events['events']['event']:
        sys.stdout.write('\rEvents:  {}/2250    Emplacements:  {}'.format(str(len(event_list)),str(len(empl_list))))
        sys.stdout.flush()
        # print '\rEvents:\t{}/2250\tEmplacements:\t{}'.format(str(len(event_list)),str(len(empl_list))),
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
    print ' '

def float2decimal(f, r='0.01', rounding=ROUND_UP ):
    r = Decimal(r)
    f = Decimal(f)
    return f.quantize(r, rounding=rounding)

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

print "Created {} categories".format(str(len(categ_list)))

for page in range(1,10):
    fetchEventsVenues(page)

for i in range(1000):
    createRandomOccurrence()

createRabais()

for i in range(1000):
    createRandomTransaction()

print "\nCategories: " + str(len(categ_list))
print "Evenements: " + str(len(event_list))
print "Emplacements:  " + str(len(empl_list)) 
print "Occurrences: " + str(len(occurence_list))
print "Rabais: " + str(len(rabais_list))
print "Transactions: " + str(len(transaction_list))

# Files printing
with open('output/clients.sql', 'w+') as f:
    for e in client_list:
        print >>f, e.INSERT_str('client')

with open('output/evenements.sql', 'w+') as f:
    for e in event_list:
        print >>f, e.INSERT_str('evenement')

with open('output/categories.sql', 'w+') as f:
    for e in categ_list:
        print >>f, e.INSERT_str('categorie')

with open('output/emplacements.sql', 'w+') as f:
    for e in empl_list:
        print >>f, e.INSERT_str('emplacement')

with open('output/occurences.sql', 'w+') as f:
    for e in occurence_list:
        print >>f, e.INSERT_str('occurence')

with open('output/transactions.sql', 'w+') as f:
    for e in transaction_list:
        print >>f, e.INSERT_str('transaction')

with open('output/rabais.sql', 'w+') as f:
    for e in rabais_list:
        print >>f, e.INSERT_str('rabais')

