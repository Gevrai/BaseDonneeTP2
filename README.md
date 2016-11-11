
## Ouvrir le projets dans sqldeveloper

File > Data Modeler > Open > Diagrammes.dmd

View > Data Modeler > Browser

## Génération de données (faker et eventful.com)


###faker

```
git clone https://github.com/joke2k/faker.git
sudo python setup.py install
```

Pour générer des données un peu plus 'vrais' que des string aléatoires, on va chercher des vrais données!

###eventful API
```
pip install simplejson
pip install httplib2
wget http://api.eventful.com/libs/python/eventfulpy-0.3.tar.gz
tar -xf eventfulpy-0.3.tar.gz
python setup.py 
```

Normalement c'est tout ce qu'il faut pour rouler le générateur, en plus d'un accès internet pour l'API
