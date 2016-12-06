-- Afficher le nombre de transactions d’achats des 5 dernières semaines ;
SELECT count(*) as "Nombre de transactions des 5 dernieres semaines" FROM transaction
WHERE (SYSDATE - dateEtHeure) < INTERVAL '35' DAY;

-- Afficher le nombre de clients utilisateurs de Google ;
SELECT count(*) as "Nombre de clients utilisateurs de google"  FROM client
WHERE courriel LIKE '%@gmail.%';

-- Afficher les clients de l'arrondissement “B4” (indiqué par le code postale commençant par “B4”) et qui n'ont pas un compte google ;
SELECT noClient, nom, prenom FROM client, adresse
WHERE client.noAdresse = adresse.noAdresse
AND codePostal LIKE 'B4%'
AND courriel NOT LIKE '%@gmail.%';

-- Afficher les noms des sous-catégories de la catégorie Sport ;
SELECT nom FROM categorie
WHERE parent = (
    SELECT noCategorie FROM categorie
    WHERE nom = 'Sports' or nom = 'Sport');

-- Afficher les emplacements de Montréal qui accueillent plus que 2000 clients.
SELECT nom FROM emplacement, adresse
WHERE emplacement.noAdresse = adresse.noAdresse
AND ville = 'Montreal'
AND capacite > 2000;

-- Afficher les informations des évènements qui ont plus de 4 occurrences et dont le prix est supérieur à $150 avant rabais ;
SELECT * FROM evenement
WHERE noEvenement IN (
    SELECT DISTINCT noEvenement
    FROM occurence
    WHERE prix > 150
    GROUP BY noEvenement
    HAVING COUNT(noEvenement) > 4
); 

-- Calculer les économies faites par un client de votre choix (id=5) grâce aux coupons rabais de toutes ses transactions;
SELECT SUM(cout-montantPaye) as "Economies faites par le client 5 grace a ces coupons"
FROM transaction
GROUP BY noClient
HAVING noClient = 5;

-- Afficher les informations des évènements qui ont plus de 4 occurrences en Ontario et dont le prix est inférieur à $150 après le rabais “âge d’or”.
SELECT * from evenement
WHERE NoEvenement IN (
    SELECT DISTINCT occurence.noEvenement FROM occurence,emplacement,adresse
    WHERE occurence.noEmplacement = emplacement.noEmplacement
    AND emplacement.noAdresse = adresse.noAdresse
    AND (adresse.province = 'ON' OR adresse.province = 'Ontario')
    AND occurence.prix < 150*(SELECT Rabais FROM coupon WHERE description = 'age d''or')
    GROUP BY occurence.noEvenement
    HAVING COUNT(occurence.noEvenement) > 4
);

-- Calculer et afficher les revenus totaux des emplacements pour tous les évènements triés par ordre décroissant. (PS. Faites attention aux statut des transactions).
WITH transaction_payee AS (
    SELECT * FROM transaction 
    WHERE (transaction.statut = 'payee' OR transaction.statut = 'approuvee')
)
SELECT emplacement.nom, SUM(transaction_payee.montantPaye) as "Revenus total"
FROM transaction_payee, occurence, emplacement
WHERE emplacement.noEmplacement = occurence.noEmplacement
AND transaction_payee.noOccurence = occurence.noOccurence
GROUP BY emplacement.noEmplacement, emplacement.nom
ORDER BY SUM(transaction_payee.montantPaye) DESC;

-- Afficher l'arborescence de toutes les catégories et toutes leurs sous-categories.
SELECT rpad(' ', level-1) || nom as Nom FROM Categorie
START WITH Parent is null
CONNECT BY PRIOR NoCategorie = Parent;
