import paramiko
from datetime import datetime
import os
import sys

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

def main():
    # Récupération des variables d'environnement
    hote = os.getenv('SSH_HOST')
    utilisateur = os.getenv('SSH_USER')
    mot_de_passe = os.getenv('SSH_PASSWORD')
    
    if not all([hote, utilisateur, mot_de_passe]):
        print("Variables d'environnement manquantes!")
        print("Veuillez définir SSH_HOST, SSH_USER et SSH_PASSWORD")
        sys.exit(1)
    
    print(f"\nConnexion à {hote}...")
    
    try:
        # Connexion SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hote, username=utilisateur, password=mot_de_passe)
        print(f"Connecté à {hote} à {datetime.now()}")
        
        # Exécution automatique pour CI/CD
        print("\nExécution des commandes de vérification...")
        executer_commande_ssh(ssh, 'tasklist')
        executer_commande_ssh(ssh, 'wmic logicaldisk get size,freespace,caption')
                
    except paramiko.AuthenticationException:
        print("Erreur d'authentification: identifiants incorrects")
        sys.exit(1)
    except paramiko.SSHException as e:
        print(f"Erreur SSH: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        sys.exit(1)
    finally:
        try:
            ssh.close()
            print("Connexion fermée.")
        except:
            pass

if __name__ == "__main__":
    main()