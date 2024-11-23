# Importation de la bibliothèque pour écouter les événements du clavier
from pynput.keyboard import Listener, Key

# Fonction appelée lorsqu'une touche est pressée
def on_press(key):

    try:
        # Affichage d'une touche standard appuyée
        print(f"Touche '{key.char}' appuyée")

    except AttributeError:

          # Affichage d'une touche speciale appuyée
        print(f"Touche spéciale '{key}' appuyée")

# Fonction appelée lorsqu'une touche est relâchée
def on_release(key):

    # Vérification si la touche relâchée est 'Échap' (Escape) pour quitter
    if key == Key.esc:
        return False

# Création d'un listener pour capturer les événements du clavier
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
