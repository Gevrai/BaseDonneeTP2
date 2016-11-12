-- Afficher le nombre de transactions d’achats des 5 dernières semaines ;
SELECT count(*)
FROM transaction
WHERE dateEtHeure > (SELECT CURRENT_TIMESTAMP FROM DUAL);

-- Afficher le nombre de clients utilisateurs de Google ;
SELECT count(*)
FROM client 
WHERE couriel LIKE '%@google.%';

-- Afficher les clients de l'arrondissement “B4” (indiqué par le code postale commençant par “B4”) et qui n'ont pas un compte google ;
SELECT clientID, nom, prenom
FROM client
WHERE codePostal LIKE 'B4%'
AND couriel NOT LIKE '%@google.%';

-- Afficher les noms des sous-catégories de la catégorie Sport ;
SELECT categorie FROM categorie
WHERE surCategorie = 'Sport';

-- Afficher les emplacements de Montréal qui accueillent plus que 2000 clients.
SELECT nom FROM emplacement
WHERE capacite > 2000;

-- Afficher les informations des évènements qui ont plus de 4 occurrences et dont le prix est supérieur à $150 avant rabais ;
SELECT * FROM evenement
WHERE evenementID IN (
    SELECT DISTINCT evenementID FROM occurence
    GROUP BY evenementID HAVING COUNT(evenementID > 4))

-- Calculer les économies faites par un client de votre choix grâce aux coupons rabais de toutes ses transactions ;

-- Afficher les informations des évènements qui ont plus de 4 occurrences en Ontario et dont le prix est inférieur à $150 après le rabais “âge d’or”.
WITH 
    tauxRabaisAgeDor as (
        SELECT tauxRabais FROM rabais WHERE description = "age d'or"), 
    even_plusQue4 as (
        SELECT evenementID FROM occurence GROUP BY evenementID HAVING count(evenementID) > 4)
SELECT * FROM evenement
WHERE 
-- Calculer et afficher les revenus totaux des emplacements pour tous les évènements triés par ordre décroissant. (PS. Faites attention aux statut des transactions).
-- Afficher l'arborescence de toutes les catégories et toutes leurs sous-categories.
