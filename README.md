# Azure Project
Ce projet a été developpé dans le cadre du de la semaine thématique Azure.
L'objectif du projet était de développer une application en utilisant Azure Comme cloud provider.

## Membres du groupe :
- Hakim SAGHIR
- Syphax SARNI

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
