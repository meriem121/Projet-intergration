import paramiko
from datetime import datetime

# Configuration de la connexion
HOTE = "192.168.0.175"
UTILISATEUR = "administrateur"
MOT_DE_PASSE = "zomita"

def afficher_menu():
    print("\nMenu Principal:")
    print("1. Voir les processus en cours")
    print("2. Voir l'espace disque")
    print("3. Options d'administration")
    print("4. Quitter")

def executer_commande_ssh(ssh, commande):
    """Exécute une commande via SSH et affiche le résultat"""
    entrees, sortie, erreur = ssh.exec_command(commande)
    print(sortie.read().decode('utf-8', errors='replace'))
    if erreur.read():
        print("Erreur:", erreur.read().decode('utf-8', errors='replace'))

def menu_surveillance(ssh):
    while True:
        print("\nSurveillance système:")
        print("1. Liste des processus (tasklist)")
        print("2. Espace disque (wmic)")
        print("3. Retour")
        
        choix = input("Votre choix (1-3): ")
        
        if choix == '1':
            executer_commande_ssh(ssh, 'tasklist')
        elif choix == '2':
            executer_commande_ssh(ssh, 'wmic logicaldisk get size,freespace,caption')
        elif choix == '3':
            break
        else:
            print("Choix invalide!")

def menu_admin(ssh):
    while True:
        print("\nAdministration:")
        print("1. Redémarrer")
        print("2. Éteindre")
        print("3. Retour")
        
        choix = input("Votre choix (1-3): ")
        
        if choix == '1':
            executer_commande_ssh(ssh, 'shutdown /r /t 0')
            print("Redémarrage demandé!")
            break
        elif choix == '2':
            executer_commande_ssh(ssh, 'shutdown /s /t 0')
            print("Extinction demandée!")
            break
        elif choix == '3':
            break
        else:
            print("Choix invalide!")

def main():
    print(f"\nConnexion à {HOTE}...")
    
    try:
        # Connexion SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOTE, username=UTILISATEUR, password=MOT_DE_PASSE)
        print(f"Connecté à {HOTE} à {datetime.now()}")
        
        while True:
            afficher_menu()
            choix = input("Votre choix (1-4): ")
            
            if choix == '1':
                executer_commande_ssh(ssh, 'tasklist')
            elif choix == '2':
                executer_commande_ssh(ssh, 'wmic logicaldisk get size,freespace,caption')
            elif choix == '3':
                menu_admin(ssh)
            elif choix == '4':
                print("Déconnexion...")
                break
            else:
                print("Choix invalide!")
                
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        ssh.close()
        print("Connexion fermée.")

if __name__ == "__main__":
    main()