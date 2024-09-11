#!/bin/bash

sudo apt-get install python3-tk
sudo apt-get install sqlite3


# Asegúrate de que pip está actualizado
python3 -m pip install --upgrade pip

# Instalar los paquetes desde requirements.txt
pip install -r requirements.txt

echo "Todos los paquetes necesarios han sido instalados."
