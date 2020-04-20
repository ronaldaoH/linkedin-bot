echo "[+] Instalador"
echo "[+] Instalando pip"
python get-pip.py
echo "[+] Instalarndo entorino virtual..."
pip install pipenv
echo "[+] Instalando paquetes..."
pipenv shell
echo "[=========] TERMINO "
