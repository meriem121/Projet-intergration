# Système de Surveillance et d'Administration à Distance

## 📌 Description
Outil Python pour surveiller et administrer des machines distantes via SSH, avec les fonctionnalités suivantes :
- Surveillance des processus système
- Analyse de l'espace disque
- Gestion des services (redémarrage/arrêt)
- Consultation des logs système

## 🛠 Prérequis
- Python 3.8+
- Packages requis :
  ```bash
  pip install paramiko
 # Docker
docker run --rm yourusername/system-monitor \
  --host <IP> \
  --user <USER> \
  --password <PASSWORD> 