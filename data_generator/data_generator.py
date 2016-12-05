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

# Global variables
client_list = []
event_list = [] 
categ_list = []
empl_list = []
occurence_list = []
transaction_list = []
rabais_list = []
amtAdressCreated = 0

def general_INSERT_str(tableName, columnNames, values):
    # Test if valid input
    assert(len(columnNames) == len(values)),"Error inserting into '{}':\nColumn (size {}):\t{}\nValues (size {}):\t{}".format(
            tableName, str(len(columnNames)), str(columnNames), str(len(values)), str(values)) 
    assert(columnNames),"Nothing to INSERT into '{}' table!".format(tableName)
    # Test if columns are right ammounts
    if (not((tableName == "adresse" and len(columnNames) == 6) or
            (tableName == "categorie" and len(columnNames) == 3) or
            (tableName == "client" and len(columnNames) == 8) or
            (tableName == "coupon" and len(columnNames) == 4) or
            (tableName == "emplacement" and len(columnNames) == 7) or
            (tableName == "evenement" and len(columnNames) == 7) or
            (tableName == "occurence" and len(columnNames) == 5) or
            (tableName == "transaction" and len(columnNames) == 10))):
        print "error printing into {} : trying to insert {} columns".format(tableName, len(columnNames))

    # Making sure every element is a string with correct format
    cols_str, vals_str = ([],[])
    for e in columnNames:
        cols_str.append(str(e))
    for e in values:
        if (isinstance(e,int)):
            vals_str.append(str(e))
        elif (e == 'None' or not e):
            vals_str.append("NULL")
        elif (isinstance(e, basestring)):
            if (("INTERVAL '" in e) or ("to_date" in e)):
                vals_str.append(e)
            else:
                vals_str.append("'{}'".format(
                    e.replace("&","e").replace("'","''").replace(";","")))
        else:
            vals_str.append(str(e))

    return "INSERT INTO {}\n({})\nVALUES\n({});\n".format(
            tableName, ', '.join(cols_str), ', '.join(vals_str))

class Client():
    def __init__(self, id):
        global fake
        global amtAdressCreated
        amtAdressCreated += 1
        self.adressID = amtAdressCreated

        self.clientID = id
        self.nom = fake.last_name()
        self.prenom = fake.first_name()
        self.couriel = fake.free_email()
        self.password = fake.password(length=10)
        self.numCivique = fake.building_number()
        self.rue = fake.street_name()[:256]
        self.codePostal = fake.postalcode().replace(" ","")
        self.ville = fake.city()[:20]
        self.province = fake.province_abbr()[:40]
        self.numTel = fake.phone_number()

    def INSERT_str(self, tableName):
        # Table Addresse
        columnNames = ['noAdresse','noCivique','rue','codePostal','ville','province']
        values = [self.adressID, self.numCivique[:10],self.rue,self.codePostal.replace(' ','')[:7],self.ville,self.province]
        insertString = general_INSERT_str('adresse', columnNames, values)

        # Table client -> tableName
        columnNames = ['NoClient','nomUtilisateur','nom','prenom','courriel','motDePasse','NoAdresse','numTel']
        values = [self.clientID, (self.nom+'.'+self.prenom)[:20], self.nom, self.prenom, self.couriel, self.password, self.adressID, self.numTel]
        return insertString + general_INSERT_str(tableName, columnNames, values)
        
class Evenement():
    def __init__(self, e, id):
        self.evenementID = id
        self.titre = e['title'][:50]
        self.description = e['description']
        if (self.description):
            self.description = self.description[:512]
        self.siteWeb = e['url']
        if (self.siteWeb):
            self.siteWeb = self.siteWeb[:256]
        self.duree = "INTERVAL '" + random.choice(['01:00','01:30','02:00','02:30','03:00','04:00','06:00','10:00','24:00','48:00']) + "' HOUR TO MINUTE" 
        global categ_list
        for c in categ_list:
            if (c.APIname == e['categories']['category'][0]['name']):
                self.noCategorie = c.id
                return
        assert(true), "Categorie '{}' inexistante".format(e['categories']['category'][0]['name']) 

    def INSERT_str(self, tableName):
        columnNames = ['noEvenement', 'titre', 'description', 'siteWeb', 'duree','imageAffiche', 'noCategorie']
        values = [self.evenementID, self.titre, self.description, self.siteWeb, self.duree,None,self.noCategorie] 
        return general_INSERT_str(tableName, columnNames, values)

class Categorie():
    def __init__(self, cat):
        global categ_list
        self.id = len(categ_list)
        self.APIname = cat
        cat = cat.replace('&amp;','and').split(': ',1)
        if(len(cat) == 2):
            self.categorie = cat[1]
            for c in categ_list:
                if (c.categorie == cat[0]):
                    self.surCategorie = c.id
        else: 
            self.categorie = cat[0]
            self.surCategorie = None

    def INSERT_str(self, tableName):
        columnNames = ['noCategorie','parent', 'nom']
        values = [self.id, self.surCategorie, self.categorie] 
        return general_INSERT_str(tableName, columnNames, values)

class Occurence():
    def __init__(self, id, evenementID, emplacementID, start_time=None, prix = None):
        global fake
        self.occurenceID = id
        if (start_time == None):
            # TODO check date syntax -> probably TIMESTAMP '2003-01-01 2:00:00'
            self.dateEtHeure =("to_date('" 
                    + fake.date_time_between_dates(datetime(2016,01,01),datetime(2020,12,30)).isoformat(':')
                    + "', 'yyyy-mm-dd hh24:mi:ss')")
        else:
            # self.dateEtHeure = start_time
            self.dateEtHeure =("to_date('" 
                    + fake.date_time_between_dates(datetime(2016,01,01),datetime(2020,12,30)).isoformat(':')
                    + "', 'yyyy-mm-dd hh24:mi:ss')")

        self.prix = float2decimal(random.uniform(5.0,75.0))
        self.evenementID = evenementID
        self.emplacementID = emplacementID

    def INSERT_str(self, tableName):
        if (not self.emplacementID):
            self.emplacementID = random.randint(0,len(empl_list))

        columnNames = ['noOccurence', 'dateEtHeure', 'prix', 'noEvenement', 'noEmplacement']
        values = [self.occurenceID, self.dateEtHeure, self.prix, self.evenementID, self.emplacementID] 
        return general_INSERT_str(tableName, columnNames, values)

class Emplacement():
    def __init__(self, e, id):
        global fake
        global amtAdressCreated
        amtAdressCreated += 1
        self.adressID = amtAdressCreated

        self.emplacementID = id
        self.siteID = e['id'] 
        self.nom = e['venue_name'][:50]
        self.siteWeb = e['url'][:256]
        self.courriel = fake.free_email()[:256]
        self.capacite = random.choice([50,100,200,300,500,1000,2000,5000,10000,15000])
        if (e['address'] != None):
            address = e['address'].split(' ',1)
            if (len(address) == 2):
                self.numCivique = address[0]
                self.rue = address[1]
            else:
                self.numCivique = fake.building_number()
                self.rue = fake.street_name()
            self.codePostal = e['postal_code']
            if (self.codePostal):
                self.codePostal.replace(" ",'')
            else:
                self.codePostal = fake.postalcode().replace(" ","");
            self.ville = e['city_name']
            self.province = e['region_abbr']
        else:
            self.numCivique = fake.building_number()
            self.rue = fake.street_name()
            self.codePostal = fake.postalcode().replace(" ","")
            self.ville = fake.city()
            self.province = fake.province_abbr()

        self.numTel = fake.phone_number()[:31]

    def INSERT_str(self, tableName):
        # Table Addresse
        columnNames = ['noAdresse','noCivique','rue','codePostal','ville','province']
        values = [self.adressID, self.numCivique[:10],self.rue,self.codePostal.replace(' ','')[:7],self.ville,self.province]
        insertString = general_INSERT_str('adresse', columnNames, values)

        # Table occurrence -> tableName
        columnNames = ['noEmplacement', 'nom', 'siteWeb', 'capacite','NoAdresse', 'numTel','courriel']
        values = [self.emplacementID, self.nom, self.siteWeb, self.capacite, self.adressID, self.numTel,self.courriel] 
        return insertString + general_INSERT_str(tableName, columnNames, values)

class Transaction():
    def __init__(self, transactionID, clientID, occurenceID, prix, codeRabais=None):
        global fake
        self.transactionID = transactionID 
        self.clientID = clientID
        self.occurenceID = occurenceID
        self.nbBillets = Decimal(str(random.randint(1,8)))
        self.statut = random.choice(["en attente","payee","approuvee","annulee"])
        self.codeRabais = codeRabais
        self.cout = prix*self.nbBillets
        if (codeRabais == None):
            self.montantPayee = prix*self.nbBillets
        else:
            tauxRabais = Decimal('1')
            for c in rabais_list:
                if (c.code == codeRabais):
                    tauxRabais = float2decimal(c.tauxRabais)
            self.montantPayee = self.cout*tauxRabais
        # TODO check date syntax -> probably TIMESTAMP '2003-01-01 2:00:00'
        self.dateEtHeure =("to_date('" 
                + fake.date_time_between_dates(datetime(2012,01,01),datetime(2016,10,30)).isoformat(':')
                + "', 'yyyy-mm-dd hh24:mi:ss')")
        self.modePaiement = random.choice(['comptant','credit','debit'])

    def INSERT_str(self, tableName):
        columnNames = ['noTransaction', 'noClient', 'noOccurence', 'statut', 'codeCoupon', 'cout','montantPaye', 'dateEtHeure', 'modePaiement','nbBillets']
        values = [self.transactionID, self.clientID, self.occurenceID, self.statut, self.codeRabais, self.cout, self.montantPayee, self.dateEtHeure, self.modePaiement,self.nbBillets]
        return general_INSERT_str(tableName, columnNames, values)

class Rabais():
    def __init__(self, code, nom, taux):
        global fake
        self.code = code
        self.nom = nom 
        self.tauxRabais = taux
        self.expiration =("to_date('" 
                + fake.date_time_between_dates(datetime(2016,01,01),datetime(2020,12,30)).date().isoformat()
                + "','yyyy-mm-dd')")

    def INSERT_str(self, tableName):
        columnNames = ['codeCoupon', 'Rabais', 'expiration','description']
        values = [self.code, self.tauxRabais, self.expiration,self.nom[:10]] 
        return general_INSERT_str(tableName, columnNames, values)

def fetchEventsVenues(page=1, maxevent=None):
    # Remplissage d'evenements et de leur emplacement en meme temps
    events = simplejson.load(open('json/event_page'+str(page)+'.json', 'r'))
    global event_list
    global empl_list
    for event in events['events']['event']:
        # Print progress
        cur = 20*len(event_list)/2250
        progress = "\r[{}{}] {}/2250".format('#'*cur, '-'*(20-cur), len(event_list))
        sys.stdout.write(progress)
        sys.stdout.flush()
        # Make current event
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
    assert(True), "Couldn't find {} in emplacement list".format(siteID)

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
    coupons = ["age d'or","etudiant","employe","membre","special","ouverture"]
    taux = [0.65,0.7,0.5,0.9,0.95,0.6]
    for i in range(len(coupons)):
        r = Rabais(i, coupons[i],taux[i])
        rabais_list.append(r)

def getTauxRabaisFromID(rabaisID):
    global rabais_list
    for r in rabais_list:
        if (r.code == rabaisID):
            return float2decimal(r.tauxRabais)
    return Decimal('1')

def createRandomTransaction():
    global event_list 
    global empl_list 
    global occurence_list
    global transaction_list
    global rabais_list

    c = random.choice(client_list)
    o = random.choice(occurence_list)

    if (random.random() > 0.75):
        codeRabais = random.choice(rabais_list).code
        prixTrans = o.prix*getTauxRabaisFromID(codeRabais)
    else:
        codeRabais = None
        prixTrans = o.prix

    t = Transaction(
            transactionID = len(transaction_list),
            clientID = c.clientID,
            occurenceID = o.occurenceID,
            prix = prixTrans,
            codeRabais=codeRabais)

    transaction_list.append(t)


nb_clients = 1000
nb_randOccurrences = 1000
nb_randTransactions = 3000
max_events = None

# Remplissage de clients
print 'Creation de {} clients'.format(nb_clients)
for id in range(nb_clients):
    cur = 20* id/(nb_clients-1)
    progress = "\r[{}{}]".format('#'*cur, '-'*(20-cur))
    sys.stdout.write(progress)
    sys.stdout.flush()
    client_list.append(Client(id))

# Remplissage de categories a partir du fichier 'categories.json'
categories = simplejson.load(open('json/categories.json', 'r'))
for categ in categories['category']:
    c = Categorie(categ['name'])
    categ_list.append(c)

print "\nCréation de {} categories".format(str(len(categ_list)))
print "[{}]".format('#'*20)

print "Création des evénements, emplacements et occurences associées"
for page in range(1,10):
    fetchEventsVenues(page, 100)
print ''

for i in range(nb_randOccurrences):
    createRandomOccurrence()

createRabais()

for i in range(nb_randTransactions):
    createRandomTransaction()

print "\nCategories: " + str(len(categ_list))
print "Evenements: " + str(len(event_list))
print "Emplacements:  " + str(len(empl_list)) 
print "Occurrences: " + str(len(occurence_list))
print "Rabais: " + str(len(rabais_list))
print "Transactions: " + str(len(transaction_list))

# Files printing
print "\nImpression dans fichier '../peuplement.sql'"
with open ('../peuplement.sql', 'w+') as p:
    print >>p, "set sqlblanklines on"
    s =""
    print "\nImpression dans fichier 'output/clients.sql'"
    with open('output/clients.sql', 'w+') as f:
        for e in client_list:
            s = e.INSERT_str('client')
            print >>f,s
            print >>p,s

    print "Impression dans fichier 'output/categories.sql'"
    with open('output/categories.sql', 'w+') as f:
        for e in categ_list:
            s = e.INSERT_str('categorie')
            print >>f,s
            print >>p,s

    print "Impression dans fichier 'output/couponRabais.sql'"
    with open('output/couponRabais.sql', 'w+') as f:
        for e in rabais_list:
            s = e.INSERT_str('coupon')
            print >>f,s
            print >>p,s

    print "Impression dans fichier 'output/evenements.sql'"
    with open('output/evenements.sql', 'w+') as f:
        for e in event_list:
            s = e.INSERT_str('evenement')
            print >>f,s
            print >>p,s

    print "Impression dans fichier 'output/emplacements.sql'"
    with open('output/emplacements.sql', 'w+') as f:
        for e in empl_list:
            s = e.INSERT_str('emplacement')
            print >>f,s
            print >>p,s

    print "Impression dans fichier 'output/occurences.sql'"
    with open('output/occurences.sql', 'w+') as f:
        for e in occurence_list:
            s = e.INSERT_str('occurence')
            print >>f,s
            print >>p,s

    print "Impression dans fichier 'output/transactions.sql'"
    with open('output/transactions.sql', 'w+') as f:
        for e in transaction_list:
            s = e.INSERT_str('transaction')
            print >>f,s
            print >>p,s
