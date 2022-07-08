# Azure Project
Ce projet a été developpé dans le cadre de la semaine thématique Azure (4IABD - ESGI).
L'objectif du projet était de développer une application en utilisant Azure Comme cloud provider.

## Membres du groupe :
- Hakim SAGHIR
- Syphax SARNI

## Fonctionnalités de l'application :
- Chargement d'images : Charger des images, rechercher des tags sur ces images en utilisant la vision par ordinateur de azure
- Recherche full text : Rechercher des images par tags (ex : cat dog animal) ou par nom de l'image (ex : image1.png)
- Suppression d'images


## Installation :

### Lancement sur windows :
```
pip install Azure_Project/requirements.txt
Azure_Project/run_windows.ps1
```

### Sur Docker :
```
docker build -t azureproject:1.0 . 
docker run -d -p 80:52800 --name azureproject azureproject:1.0
```
