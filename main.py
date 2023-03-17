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

def limpiarPantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mainOptions():
    print("Welcome to Switch2SD: ") 
    print("Please select one of the following options: \n")
    print("1. [Erista Unpatched] CFW emuNAND + OFW sysNAND")
    print("2. [Erista Unpatched] CFW emuNAND + CFW sysNAND")
    print("3. [Erista Unpatched] CFW sysNAND\n")
    print("4. [SXCore & HWFly] CFW emuNAND + OFW sysNAND")
    print("5. [SXCore & HWFly] CFW emuNAND + CFW sysNAND")
    print("6. [SXCore & HWFly] CFW sysNAND\n\n")

    opcion = input("Insert the number of the option you want to select (1-6):")
    if opcion not in ["1", "2", "3", "4", "5", "6"]:
        print("Invalid option. Please, insert a valid option number (1-6).")
        limpiarPantalla()
        opcion = mainOptions()
    else:
        limpiarPantalla()
        print("You selected option {}.".format(opcion))
    return opcion

def homebrewOptions():
    opciones = [
        {"valor": 1, "nombre": "Tinfoil [May be slow]", "seleccionada": False},
        {"valor": 2, "nombre": "Homebrew Store", "seleccionada": False},
        {"valor": 3, "nombre": "Goldleaf", "seleccionada": False}
    ]
    
    while True:
        print("Select the homebrew apps you want to download: \n")      
        for opcion in opciones:
            check = "[X]" if opcion["seleccionada"] else "[ ]"
            print(f"{check} {opcion['valor']}. {opcion['nombre']}")
        
        opcion = input("Insert the number of the option you want to select (1-3) or press enter to continue: ")
        limpiarPantalla()
        if opcion == "":
            break
        elif opcion not in ["1", "2", "3"]:
            print("Invalid option. Please, insert a valid option number (1-3).")
            continue
        opcion = int(opcion)
        opciones[opcion-1]["seleccionada"] = not opciones[opcion-1]["seleccionada"]
        
    opciones_seleccionadas = [opcion["valor"] for opcion in opciones if opcion["seleccionada"]]
    return opciones_seleccionadas

def dwSXGear(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    print("--- (Skip this if you use a HWFLY modchip) ---")
    value = input("Do you want to download SX Gear? (Y/N): ")
    if value in ["s", "S", "y", "Y"]:
        downloadZip(
            "https://web.archive.org/web/20210217231219/https://sx.xecuter.com/download/SX_Gear_v1.1.zip",
            os.path.join(tempFolder, "sxgear_v1.1.zip"),
            destFolder,
            "SX"
        )
        return True

    sleep(5)
    return False

def mkFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def delFolder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)

def getVersion(url, regex, hekate=False):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    release_title = soup.find('h1', class_='d-inline mr-3').text.strip()
    version = re.search(regex, release_title).group(1)
    if hekate:
        nyx_version = re.search(r'Nyx v([\d.]+)', release_title).group(1)
        return version, nyx_version
    else:
        return version
    
def downloadFile(dw_url, dw_path, dest_folder, url):
    try:
        urllib.request.urlretrieve(dw_url, dw_path)
    except FileExistsError:
        print("[?] {} already exists".format(url))
        pass
    except Exception as e:
        return "[!] Error downloading {}: {}".format(url, e)
    
    if url == "Fusee":
        folder = dest_folder + "/bootloader/payloads/"
    else:
        folder = dest_folder + "/switch/{}".format(url)

    mkFolder(folder)
    shutil.copy2(dw_path, folder)
    return "[OK] {} downloaded successfully.".format(url)

def downloadZip(dw_url, dw_path, dest_folder, url):
    try:
        urllib.request.urlretrieve(dw_url, dw_path)
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
    hekate_version, nyx_version = getVersion(url, r'hekate v([\d.]+)', hekate=True)
    return downloadZip(
        f"https://github.com/CTCaer/hekate/releases/download/v{hekate_version}/hekate_ctcaer_{hekate_version}_Nyx_{nyx_version}.zip",
        os.path.join(tempFolder, "hekate{}.zip".format(hekate_version)),
        destFolder,
        "Hekate"
    )

def dwAtmosphere(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    url = "https://github.com/Atmosphere-NX/Atmosphere/releases/latest"
    atmosphere_version = getVersion(url, r'Atmosphère ([\d.]+)')
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

def dwFusee(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    url = "https://github.com/Atmosphere-NX/Atmosphere/releases/latest"
    atmosphere_version = getVersion(url, r'Atmosphère ([\d.]+)')
    return downloadFile(
        f"https://github.com/Atmosphere-NX/Atmosphere/releases/download/{atmosphere_version}/fusee.bin",
        os.path.join(tempFolder, "fusee.bin"),
        destFolder,
        "Fusee"
    )

def dwSigpatches(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    return downloadZip(
        "https://sigmapatches.coomer.party/sigpatches.zip",
        os.path.join(tempFolder, "sigpatches{}.zip".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))),
        destFolder,
        "Sigpatches"
    )

def dwTinfoil(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    url = "https://tinfoil.io/Download#download"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all 'a' tags with the specified class
    buttons = soup.find_all('a', class_='btn btn-info-gradiant btn-md btn-arrow')

    # Extract the 'href' attribute of the button containing the specific text
    download_url = None
    search_text = "NRO (Self Installer)"

    for button in buttons:
        span_text = button.find('span').text
        if search_text in span_text:
            download_url = button['href']
            break

    if download_url is None:
        print("[!] Could not find the specified button.")
    else:
        # Download the zip file using the download URL
        dw_path = tempFolder + "/tinfoil_self_installer.zip"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        try:
            print("[i] Tinfoil NRO (Self Installer) starting download...")
            response = requests.get("https:" + download_url, headers=headers)
            with open(dw_path, 'wb') as f:
                f.write(response.content)
            print("[OK] Tinfoil NRO (Self Installer) downloaded successfully.")
        except Exception as e:
            print("[!] Error downloading Tinfoil NRO (Self Installer): {}".format(e))
    
    with zipfile.ZipFile(dw_path, 'r') as zip_ref:
        zip_ref.extractall(destFolder)

    return "[OK] Tinfoil NRO (Self Installer) copied successfully."

def dwAppStore(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    url = "https://github.com/fortheusers/hb-appstore/releases/latest"
    appstore_version = getVersion(url, r'Homebrew App Store ([\d.]+)')
    return downloadFile(
        f"https://github.com/fortheusers/hb-appstore/releases/download/{appstore_version}/appstore.nro",
        os.path.join(tempFolder, "appstore{}.zip".format(appstore_version)),
        destFolder,
        "appstore"
    )

def dwGoldLeaf(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    return downloadFile(
        "https://github.com/XorTroll/Goldleaf/releases/download/0.10/Goldleaf.nro",
        os.path.join(tempFolder, "goldleaf_v0.10.zip"),
        destFolder,
        "GoldLeaf"
    )

def writeConfig(value, config_data, destFolder="COPY_TO_SD"):
    exo_path = os.path.join(destFolder, "exosphere.ini")
    hekate_path = os.path.join(destFolder, "bootloader/hekate_ipl.ini")
    hosts_path = os.path.join(destFolder, "atmosphere/hosts/defaut.txt")
    selected_config = None

    # Find the configuration with the provided value
    for config in config_data["opciones"]:
        if config["valor"] == value:
            selected_config = config
            break

    if not selected_config:
        print("Invalid value. Configuration not found.")
        return
    
    with open(exo_path, "w") as exo_file:
        exo_file.write(selected_config["exosphere"])
        
    os.makedirs(os.path.dirname(hekate_path), exist_ok=True)
    
    with open(hekate_path, "w") as hekate_file:
        hekate_file.write(selected_config["hekate_ipl"])
        
    os.makedirs(os.path.dirname(hosts_path), exist_ok=True)
    
    with open(hosts_path, "w") as hosts_file:
        hosts_file.write(selected_config["hosts"])
    print("Configuration files written successfully.")

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

if __name__ == '__main__':
    try:
        with open('details.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print("Error loading details.json: {}".format(e))

    delFolder(folder = "COPY_TO_SD")
    mkFolder("temp")
    mkFolder("COPY_TO_SD")
    opcion = mainOptions()
    hbOpciones = homebrewOptions()
    modded = False
    if opcion in ["4", "5", "6"]:
        modded = True
        sxStatus = dwSXGear()

    if modded:
        print(sxStatus)

    print(dwHekate())
    print(dwAtmosphere())
    print(dwFusee())
    print(dwSigpatches())

    if 1 in hbOpciones:
        print(dwTinfoil())
    if 2 in hbOpciones:
        print(dwGoldLeaf())
    if 3 in hbOpciones:
        print(dwAppStore())

    writeConfig(opcion, data)

    value = input("Do you want to open COPY_TO_SD folder? (Y/N): ")
    if value in ["s", "S", "y", "Y"]:
        openFolder()
        sleep(5)

    input("Do you want to delete temp folder? (Y/N): ")
    if value in ["s", "S", "y", "Y"]:
        delFolder(folder = "temp")