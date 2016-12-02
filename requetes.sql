-- Afficher le nombre de transactions d’achats des 5 dernières semaines ;
SELECT count(*) FROM transaction
WHERE (SYSTIMESTAMP - dateEtHeure) < INTERVAL '35' DAY;

-- Afficher le nombre de clients utilisateurs de Google ;
SELECT count(*) FROM client
WHERE courriel LIKE '%@gmail.%';

-- Afficher les clients de l'arrondissement “B4” (indiqué par le code postale commençant par “B4”) et qui n'ont pas un compte google ;
SELECT noClient, nom, prenom FROM client, adresse
WHERE client.noAdresse = adresse.noAdresse
AND codePostal LIKE 'B4%'
AND courriel NOT LIKE '%@gmail.%';

-- Afficher les noms des sous-catégories de la catégorie Sport ;
SELECT nom FROM categorie
WHERE parent = 'Sport';

-- Afficher les emplacements de Montréal qui accueillent plus que 2000 clients.
SELECT nom FROM emplacement, adresse
WHERE emplacement.noAdresse = adresse.noAdresse
AND ville = 'Montreal'
AND capacite > 2000;

-- Afficher les informations des évènements qui ont plus de 4 occurrences et dont le prix est supérieur à $150 avant rabais ;
SELECT * FROM evenement
WHERE evenementID IN (
    SELECT DISTINCT evenementID
    FROM occurence
    GROUP BY evenementID
    HAVING COUNT(evenementID) > 4
    AND prix > 150) 

-- Calculer les économies faites par un client de votre choix (id=5) grâce aux coupons rabais de toutes ses transactions;
SELECT SUM(cout-montantPaye) FROM transaction
GROUP BY noClient
HAVING noClient = 5;

-- Afficher les informations des évènements qui ont plus de 4 occurrences en Ontario et dont le prix est inférieur à $150 après le rabais “âge d’or”.
SELECT * from evenement
WHERE NoEvenement IN (
      SELECT DISTINCT noEvenement FROM occurence
      GROUP BY noEvenement
      HAVING COUNT(noEvenement) > 4
      AND    Prix < 150*(SELECT Rabais from coupon where nom = 'age dor')
);


-- Calculer et afficher les revenus totaux des emplacements pour tous les évènements triés par ordre décroissant. (PS. Faites attention aux statut des transactions).
SELECT noEvenement, revenus
FROM transaction
GROUP BY noEvenement
HAVING statut = 'payee' OR statut = 'approuvee'
ORDER BY SUM(montantPaye) as revenus DESC;

-- Afficher l'arborescence de toutes les catégories et toutes leurs sous-categories.
