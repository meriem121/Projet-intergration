print("hello")
import paramiko
# Informations de connexion
hostname = "127.0.0.1"  
port = 2222             
username = "meriem"     
password = "Password1234"  

# Créer une instance SSHClient
ssh = paramiko.SSHClient()

# Ajouter la clé SSH automatiquement (pour éviter l'erreur "Unknown Host")
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Se connecter à la machine virtuelle
    ssh.connect(hostname, port=port, username=username, password=password)
    print("Connexion SSH établie avec succès ")

except paramiko.AuthenticationException:
    print("Échec de l'authentification. Vérifiez vos identifiants.")
except paramiko.SSHException as e:
    print(f"Erreur SSH : {e}")
except Exception as e:
    print(f"Erreur : {e}")
finally:
    # Fermer la connexion SSH
    ssh.close()
    print("Connexion SSH fermée.")