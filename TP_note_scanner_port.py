# Importation de la bibliothèque permettant la communication réseau et les exécutions parallèles
import socket
from concurrent.futures import ThreadPoolExecutor

# Fonction qui scanne les ports et vérifie l'état de chaque port
def scanner_port(cible, port):
    try:

        # Création d'un socket TCP/IP pour tenter une connexion avec le port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1) 

            # Connexion à l'adresse cible et affichage de l'état du port
            resultat = s.connect_ex((cible, port))
            if resultat == 0:
                print(f"[+] Port {port} ouvert")

    except Exception as e:
        pass

# Fonction qui gère le scan de plusieurs ports en parallèle
def scanneur_ports(cible, ports, threads=100):
    print(f"Scan de {cible} pour les ports : {ports} en utilisant {threads} processus en parallèle (threads)")  

    # Utilisation de ThreadPoolExecutor pour exécuter des scans en parallèles sur plusieurs ports
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(lambda p: scanner_port(cible, p), ports)

if __name__ == "__main__":
    cible_ip = input("Cible IP: ")

    # Choix de l'intervalle des ports à scanner allant de 20 à 65535
    ports_to_scan = range(20, 65535)

    # Lancement du scan des ports avec l'adresse cible et la plage définie, et un nombre de processus en parallèle (threads)
    scanneur_ports(cible_ip, ports_to_scan, threads=1500)