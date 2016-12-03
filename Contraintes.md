Contraintes
--------------
* Contraintes de clé primaires, clé étrangères
* Contraintes de "non-nullité"
  * Sur les clés primaires
  * Evenement: Titre, Duree
  * Categorie: Nom
  * Coupon: Rabais
  * Client: NomUtilisateur, MotDePasse, Courriel
  * Transaction: NoClient(clé étrangère), Statut, Cout, DateEtHeure, ModePaiement, MontantPaye, NbBillets, NoOccurence(clé étrangère)
  * Adresse: NoCivique, Rue, Ville, Province, CodePostal
  * Emplacement: NoAdresse(clé étrangère)
  * Occurence: NoEvenement(clé étrangère), NoEmplacement(clé étrangère)
* Contrainte de non-transferabilité(immutabilité):
  * Occurence: NoEvenement
  * Transaction: CodeCoupon, NoClient, NoOccurence
* Contraintes de domaine:
  * Coupon: Rabais(entre 0 et 1)
  * Transaction: Cout(supérieur à 0), MontantPaye(supérieur à 0), DateEtHeure(avant le présent, ou égal au présent), NbBillets(positif),
    Statut(dans ['annulée', 'approuvée', 'en attente', 'payée']), ModePaiement(dans ['comptant', 'credit', 'debit'])    
  * Emplacement: Capacite(supérieur à 0)
  *
  
          
  
  
