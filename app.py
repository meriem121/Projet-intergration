import paramiko
from datetime import datetime
from getpass import getpass  # Pour la saisie sécurisée du mot de passe

def afficher_menu():
    print("\nMenu Principal:")
    print("1. Voir les processus en cours")
    print("2. Voir l'espace disque")
    print("3. Options d'administration")
    print("4. Quitter")

def executer_commande_ssh(ssh, commande):
    """Exécute une commande via SSH et affiche le résultat"""
    try:
        stdin, stdout, stderr = ssh.exec_command(commande)
        output = stdout.read().decode('utf-8', errors='replace')
        if output:
            print(output)
        
        error = stderr.read().decode('utf-8', errors='replace')
        if error:
            print("Erreur:", error)
    except Exception as e:
        print(f"Erreur d'exécution: {e}")

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
            return False  # Indique que la connexion sera coupée
        elif choix == '2':
            executer_commande_ssh(ssh, 'shutdown /s /t 0')
            print("Extinction demandée!")
            return False
        elif choix == '3':
            return True
        else:
            print("Choix invalide!")

def main():
    # Saisie interactive des identifiants
    hote = input("Adresse IP de la machine: ")
    utilisateur = input("Nom d'utilisateur: ")
    mot_de_passe = getpass("Mot de passe: ")
    
    print(f"\nConnexion à {hote}...")
    
    try:
        # Connexion SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hote, username=utilisateur, password=mot_de_passe)
        print(f"Connecté à {hote} à {datetime.now()}")
        
        while True:
            afficher_menu()
            choix = input("Votre choix (1-4): ")
            
            if choix == '1':
                executer_commande_ssh(ssh, 'tasklist')
            elif choix == '2':
                executer_commande_ssh(ssh, 'wmic logicaldisk get size,freespace,caption')
            elif choix == '3':
                if not menu_admin(ssh):
                    break  # Quitter si shutdown/reboot demandé
            elif choix == '4':
                print("Déconnexion...")
                break
            else:
                print("Choix invalide!")
                
    except paramiko.AuthenticationException:
        print("Erreur d'authentification: identifiants incorrects")
    except paramiko.SSHException as e:
        print(f"Erreur SSH: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")
    finally:
        try:
            ssh.close()
            print("Connexion fermée.")
        except:
            pass

if __name__ == "__main__":
    main()