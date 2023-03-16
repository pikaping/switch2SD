import os
import re
import datetime
import json
import shutil
import zipfile
import requests
import platform
import subprocess
import urllib.request

from time import sleep
from bs4 import BeautifulSoup

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mainOptions():
    print("Bienvenido al programa de selección de opciones!")
    print("Por favor, seleccione una de las siguientes opciones: ")
    print("1. CFW emuNAND + OFW sysNAND")
    print("2. CFW emuNAND + CFW sysNAND")
    print("3. CFW sysNAND")

    opcion = input("Ingrese el número de la opción que desea seleccionar (1-3): ")
    if opcion not in ["1", "2", "3"]:
        print("Lo siento, opción inválida. Por favor, ingrese un número de opción válido (1-3).\n")
        limpiar_pantalla()
        opcion = mainOptions()

    else:
        limpiar_pantalla()
        print("Ha seleccionado la Opción " + opcion + ".\n")

    return opcion

def homebrewOptions():
    opciones = [
        {"valor": 1, "nombre": "Tinfoil", "seleccionada": False},
        {"valor": 2, "nombre": "Homebrew Store", "seleccionada": False},
        {"valor": 3, "nombre": "Goldleaf", "seleccionada": False}
    ]
    
    while True:
        print("Seleccione una o varias de las siguientes opciones: ")
        
        for opcion in opciones:
            check = "[X]" if opcion["seleccionada"] else "[ ]"
            print(f"{check} {opcion['valor']}. {opcion['nombre']}")
        
        opcion = input("Ingrese el número de la opción que desea seleccionar (1-3), o presione Enter para continuar: ")
        limpiar_pantalla()
        
        # Verificar si se ingresó una opción válida
        if opcion == "":
            break  # Salir del bucle si no se seleccionó ninguna opción más
        elif opcion not in ["1", "2", "3"]:
            print("Opción inválida. Por favor, ingrese un número de opción válido (1-3).")
            continue
        
        # Marcar la opción seleccionada y mostrar la marca de verificación en el menú
        opcion = int(opcion)
        opciones[opcion-1]["seleccionada"] = not opciones[opcion-1]["seleccionada"]
        
    # Devolver la lista de opciones seleccionadas
    opciones_seleccionadas = [opcion["valor"] for opcion in opciones if opcion["seleccionada"]]
    return opciones_seleccionadas

def mkFolders(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    if not os.path.exists(tempFolder):
        os.makedirs(tempFolder)
    if not os.path.exists(destFolder):
        os.makedirs(destFolder)

def delFolder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)

def downloadZip(download_url, dw_path, dest_folder, url):
    try:
        urllib.request.urlretrieve(download_url, dw_path)
    except FileExistsError:
        print("[?] {} already exists".format(url))
        pass
    except Exception as e:
        return "[!] Error downloading {}: {}".format(url, e)

    with zipfile.ZipFile(dw_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    return "[OK] {} downloaded successfully.".format(url)

def dwHekate(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    url = "https://github.com/CTCaer/hekate/releases/latest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    release_title = soup.find('h1', class_='d-inline mr-3').text.strip()
    hekate_version = re.search(r'hekate v([\d.]+)', release_title).group(1)
    nyx_version = re.search(r'Nyx v([\d.]+)', release_title).group(1)
    return downloadZip(
        f"https://github.com/CTCaer/hekate/releases/download/v{hekate_version}/hekate_ctcaer_{hekate_version}_Nyx_{nyx_version}.zip",
        os.path.join(tempFolder, "hekate{}.zip".format(hekate_version)),
        destFolder,
        "Hekate"
    )

def dwAtmosphere(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    url = "https://github.com/Atmosphere-NX/Atmosphere/releases/latest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    release_title = soup.find('h1', class_='d-inline mr-3').text.strip()
    atmosphere_version = re.search(r'Atmosphère ([\d.]+)', release_title).group(1)
    assets_url = f"https://github.com/Atmosphere-NX/Atmosphere/releases/expanded_assets/{atmosphere_version}"
    response = requests.get(assets_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    zip_name = soup.find('span', class_='Truncate-text text-bold').text.strip()
    return downloadZip(
        f"https://github.com/Atmosphere-NX/Atmosphere/releases/download/{atmosphere_version}/{zip_name}",
        os.path.join(tempFolder, "atmosphere{}.zip".format(atmosphere_version)),
        destFolder,
        "Atmosphere"
    )

def dwSigpatches(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    return downloadZip(
        "https://sigmapatches.coomer.party/sigpatches.zip",
        os.path.join(tempFolder, "sigpatches{}.zip".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))),
        destFolder,
        "Sigpatches"
    )

def dwAppStore(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    url = "https://github.com/fortheusers/hb-appstore/releases/latest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    release_title = soup.find('h1', class_='d-inline mr-3').text.strip()
    appstore_version = re.search(r'Homebrew App Store ([\d.]+)', release_title).group(1)
    download_url = f"https://github.com/fortheusers/hb-appstore/releases/download/{appstore_version}/appstore.nro"
    dwName = "appstore{}.zip".format(appstore_version)
    dwPath = os.path.join(tempFolder, dwName)
    try:
        urllib.request.urlretrieve(download_url, dwPath)
    except FileExistsError:
        print("[?] HB AppStore already downloaded")
        pass
    except Exception as e:
        return "[!] Error downloading HB AppStore: " + str(e)
    
    if not os.path.exists(destFolder + "/switch/appstore"):
        os.makedirs(destFolder + "/switch/appstore")
    shutil.copy2(dwPath, destFolder + "/switch/appstore/appstore.nro")
    return "[OK] HB AppStore downloaded successfully."

def dwGoldLeaf(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    download_url = "https://github.com/XorTroll/Goldleaf/releases/download/0.10/Goldleaf.nro"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    dwName = "goldleaf{}.zip".format(timestamp)
    dwPath = os.path.join(tempFolder, dwName)
    try:
        urllib.request.urlretrieve(download_url, dwPath)
    except FileExistsError:
        print("[?] GoldLeaf already downloaded")
        pass
    except Exception as e:
        return "[!] GoldLeaf download failed: " + str(e)
    
    if not os.path.exists(destFolder + "/switch/goldleaf"):
        os.makedirs(destFolder + "/switch/goldleaf")
    shutil.copy2(dwPath, destFolder + "/switch/goldleaf/Goldleaf.nro")
    return "[OK] GoldLeaf downloaded successfully."

def openFolder(folder_path="COPY_TO_SD"):
    current_platform = platform.system()

    if current_platform == "Windows":
        subprocess.Popen(["explorer", folder_path])
    elif current_platform == "Darwin":
        subprocess.Popen(["open", folder_path])
    elif current_platform == "Linux":
        subprocess.Popen(["xdg-open", folder_path])
    else:
        print(f"Unsupported platform: {current_platform}")

def main():
    try:
        with open('details.jsonc', 'r') as f:
            data = json.load(f)
            print("JSON OK")
    except Exception as e:
        print(e)
        data = {}

    delFolder(folder = "COPY_TO_SD")
    mkFolders()
    opcion = mainOptions()
    hbOpciones = homebrewOptions()

    print(dwHekate())
    print(dwAtmosphere())
    print(dwSigpatches())

    if 1 in hbOpciones:
        print("tinfoil")
    if 2 in hbOpciones:
        print(dwGoldLeaf())
    if 3 in hbOpciones:
        print(dwAppStore())


    value = input("¿Desea abrir la carpeta de destino? (S/N): ")
    if value in ["s", "S"]:
        openFolder()
        sleep(5)

    input("¿Desea eliminar la carpeta temporal? (S/N): ")
    if value in ["s", "S"]:
        delFolder(folder = "temp")


if __name__ == '__main__':
    main()



