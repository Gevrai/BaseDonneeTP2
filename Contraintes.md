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
  * Occurence: NoEvenement(clé étrangère)
* Contrainte de non-transferabilité(immutabilité):
  * Occurence: NoEvenement
  * Transaction: CodeCoupon, NoClient, NoOccurence
* Contraintes de domaine:
  * Coupon: Rabais(entre 0 et 1, 0 exclu)
  * Transaction: Cout(positif), DateEtHeure(avant le temps présent, ou égal au temps présent),
    Statut(valeurs dans ['annulée', 'approuvée', 'en attente', 'payée']), ModePaiement(valeurs dans ['comptant', 'credit', 'debit']),
    MontantPaye(positif), NbBillets(positif)
  * Emplacement: Capacite(supérieur à 0)  
* Règles de suppression("delete rules")
  * Le retrait d'un entré de "Evenement" entraîne le retrait des occurences associées.
  * Le retrait d'une entré de "Adresse" entraîne le retrait des emplacements associés.
  * Le retrait d'un emplacement entraîne le changement de la référence dans "Occurence" à "NULL"
* Autre
  * Transaction: MontantPaye(doit être inférieur à Cout - Cout*Rabais dans le cas ou un coupon est utilisé).
  
  
  
          
  
  
