Contraintes
--------------
On assume les contraintes de type(e.g. une colonne de type "Integer" ne peut être qu'un entier...).

* Contraintes de clé primaires, clé étrangères
  * NoClient, NoEvenement, NoEmplacement, NoAdresse, NoTransaction, NoOccurence, CodeCoupon
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
  * Transaction: Cout(positif), DateEtHeure(avant le temps présent, ou égal au temps présent),
    Statut(valeurs dans ['annulée', 'approuvée', 'en attente', 'payée']), ModePaiement(valeurs dans ['comptant', 'credit', 'debit'])
    * "NbBillets" peut être négatif dans le cas d'un remboursement
    * "Cout" et"MontantPaye" peuvent être égal à zéro si "NbBillets" est égal à zéro, et négatif si "NbBillets" est négatif
  * Emplacement: Capacite(supérieur à 0)

  
          
  
  
