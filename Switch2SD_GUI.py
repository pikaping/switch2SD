import os
import re
import shutil
import zipfile
import argparse
import requests
import platform
import subprocess
import urllib.request

from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime as dt
from gooey import Gooey, GooeyParser

data = {
    "opciones": [
      {
        "valor": 1, 
        "hosts": "# Block Nintendo Servers\n127.0.0.1 *nintendo.*\n127.0.0.1 *nintendo-europe.com\n127.0.0.1 *nintendoswitch.*\n95.216.149.205 *conntest.nintendowifi.net\n95.216.149.205 *ctest.cdn.nintendo.net",
        "exosphere": "[exosphere]\ndebugmode=1\ndebugmode_user=0\ndisable_user_exception_handlers=0\nenable_user_pmu_access=0\nblank_prodinfo_sysmmc=0\nblank_prodinfo_emummc=1\nallow_writing_to_cal_sysmmc=0\nlog_port=0\nlog_baud_rate=115200\nlog_inverted=0",
        "hekate_ipl": "[config]\nautoboot=0\nautoboot_list=0\nbootwait=3\nbacklight=100\nautohosoff=0\nautonogc=1\nupdater2p=0\nbootprotect=0\n\n[Atmosphere CFW]\npayload=bootloader/payloads/fusee.bin\nicon=bootloader/res/icon_payload.bmp\n\n[Stock SysNAND]\nfss0=atmosphere/package3\nstock=1\nemummc_force_disable=1\nicon=bootloader/res/icon_switch.bmp"
      },
      {
        "valor": 2,
        "hosts": "# Block Nintendo Servers\n127.0.0.1 *nintendo.*\n127.0.0.1 *nintendo-europe.com\n127.0.0.1 *nintendoswitch.*\n95.216.149.205 *conntest.nintendowifi.net\n95.216.149.205 *ctest.cdn.nintendo.net",
        "exosphere": "[exosphere]\ndebugmode=1\ndebugmode_user=0\ndisable_user_exception_handlers=0\nenable_user_pmu_access=0\nblank_prodinfo_sysmmc=1\nblank_prodinfo_emummc=1\nallow_writing_to_cal_sysmmc=0\nlog_port=0\nlog_baud_rate=115200\nlog_inverted=0",
        "hekate_ipl": "[config]\nautoboot=0\nautoboot_list=0\nbootwait=3\nbacklight=100\nautohosoff=0\nautonogc=1\nupdater2p=0\nbootprotect=0\n\n[Atmosphere - EmuNAND]\npayload=bootloader/payloads/fusee.bin\nicon=bootloader/res/icon_payload.bmp\n\n[Atmosphere - SysNAND]\nfss0=atmosphere/package3\nemummc_force_disable=1\nicon=bootloader/res/icon_payload.bmp\n\n[Stock SysNAND]\nfss0=atmosphere/package3\nstock=1\nemummc_force_disable=1\nicon=bootloader/res/icon_switch.bmp"
      },
      {
        "valor": 3,
        "hosts": "# Block Nintendo Servers\n127.0.0.1 *nintendo.*\n127.0.0.1 *nintendo-europe.com\n127.0.0.1 *nintendoswitch.*\n95.216.149.205 *conntest.nintendowifi.net\n95.216.149.205 *ctest.cdn.nintendo.net",
        "exosphere": "[exosphere]\ndebugmode=1\ndebugmode_user=0\ndisable_user_exception_handlers=0\nenable_user_pmu_access=0\nblank_prodinfo_sysmmc=1\nblank_prodinfo_emummc=0\nallow_writing_to_cal_sysmmc=0\nlog_port=0\nlog_baud_rate=115200\nlog_inverted=0",
        "hekate_ipl": "[config]\nautoboot=0\nautoboot_list=0\nbootwait=3\nbacklight=100\nautohosoff=0\nautonogc=1\nupdater2p=0\nbootprotect=0\n\n[Atmosphere CFW]\npayload=bootloader/payloads/fusee.bin\nicon=bootloader/res/icon_payload.bmp\n\n[Stock SysNAND]\nfss0=atmosphere/package3\nstock=1\nemummc_force_disable=1\nicon=bootloader/res/icon_switch.bmp"
      },
      {
        "valor": 4, 
        "hosts": "# Block Nintendo Servers\n127.0.0.1 *nintendo.*\n127.0.0.1 *nintendo-europe.com\n127.0.0.1 *nintendoswitch.*\n95.216.149.205 *conntest.nintendowifi.net\n95.216.149.205 *ctest.cdn.nintendo.net",
        "exosphere": "[exosphere]\ndebugmode=1\ndebugmode_user=0\ndisable_user_exception_handlers=0\nenable_user_pmu_access=0\nblank_prodinfo_sysmmc=0\nblank_prodinfo_emummc=1\nallow_writing_to_cal_sysmmc=0\nlog_port=0\nlog_baud_rate=115200\nlog_inverted=0",
        "hekate_ipl": "[config]\nautoboot=0\nautoboot_list=0\nbootwait=3\nbacklight=100\nautohosoff=0\nautonogc=1\nupdater2p=0\nbootprotect=0\n\n[Atmosphere CFW]\npayload=bootloader/payloads/fusee.bin\nicon=bootloader/res/icon_payload.bmp"
      },
      {
        "valor": 5,
        "hosts": "# Block Nintendo Servers\n127.0.0.1 *nintendo.*\n127.0.0.1 *nintendo-europe.com\n127.0.0.1 *nintendoswitch.*\n95.216.149.205 *conntest.nintendowifi.net\n95.216.149.205 *ctest.cdn.nintendo.net",
        "exosphere": "[exosphere]\ndebugmode=1\ndebugmode_user=0\ndisable_user_exception_handlers=0\nenable_user_pmu_access=0\nblank_prodinfo_sysmmc=1\nblank_prodinfo_emummc=1\nallow_writing_to_cal_sysmmc=0\nlog_port=0\nlog_baud_rate=115200\nlog_inverted=0",
        "hekate_ipl": "[config]\nautoboot=0\nautoboot_list=0\nbootwait=3\nbacklight=100\nautohosoff=0\nautonogc=1\nupdater2p=0\nbootprotect=0\n\n[Atmosphere - EmuNAND]\npayload=bootloader/payloads/fusee.bin\nicon=bootloader/res/icon_payload.bmp\n\n[Atmosphere - SysNAND]\nfss0=atmosphere/package3\nemummc_force_disable=1\nicon=bootloader/res/icon_payload.bmp\n\n[Warmboot Error Fix]\nfss0=atmosphere/package3\nstock=1\nemummc_force_disable=1\nicon=bootloader/res/icon_switch.bmp"      
      },
      {
        "valor": 6,
        "hosts": "# Block Nintendo Servers\n127.0.0.1 *nintendo.*\n127.0.0.1 *nintendo-europe.com\n127.0.0.1 *nintendoswitch.*\n95.216.149.205 *conntest.nintendowifi.net\n95.216.149.205 *ctest.cdn.nintendo.net",
        "exosphere": "[exosphere]\ndebugmode=1\ndebugmode_user=0\ndisable_user_exception_handlers=0\nenable_user_pmu_access=0\nblank_prodinfo_sysmmc=1\nblank_prodinfo_emummc=0\nallow_writing_to_cal_sysmmc=0\nlog_port=0\nlog_baud_rate=115200\nlog_inverted=0",
        "hekate_ipl": "[config]\nautoboot=0\nautoboot_list=0\nbootwait=3\nbacklight=100\nautohosoff=0\nautonogc=1\nupdater2p=0\nbootprotect=0\n\n[Atmosphere CFW]\npayload=bootloader/payloads/fusee.bin\nicon=bootloader/res/icon_payload.bmp"
      }
    ]
  }

@Gooey(tabbed_groups=True, show_success_modal=False)
def parse_args():
    parser = GooeyParser(formatter_class=argparse.RawTextHelpFormatter, description="My Cool GUI Program!", prog="My Cool GUI Program")
    maingroup = parser.add_argument_group(
        "Main Options", 
        "Select the options you want to use and then click on 'Start'."
    )
    advgroup = parser.add_argument_group(
        "Advanced Options", 
        "Select the options you want to use and then click on 'Start'."
    )
    maingroup.add_argument('--Platform', default=None, choices=['Erista', 'HWFly', 'SXCore'], help='SXCore: Adds SXGear to the setup.', gooey_options={'label': 'Platform'})
    maingroup.add_argument('--NAND_Config', default=None, choices=['1. CFW EmuNAND + OFW SysNAND','2. CFW EmuNAND + CFW SysNAND','3. CFW SysNAND'], help='Choose the NAND configuration you want to use.', gooey_options={'label': 'NAND Config'})
    maingroup.add_argument('--Homebrew_Apps', widget='Listbox', nargs='*', default=None, choices=['1. Tinfoil [may be slow to download]', '2. HB App Store', '3. Goldleaf'], help='Select the Homebrew Apps you want to install.', gooey_options={'label': 'Homebrew Apps'})
    advgroup.add_argument('--Delete_temporal_files', action='store_true', default=True, help='Remove temporal files before closing.', gooey_options={'label': 'Delete temporal files'})
    advgroup.add_argument('--Open_folder', action='store_true', default=True, help='Open COPY_TO_SD folder before closing.', gooey_options={'label': 'Open folder'})
    return parser.parse_args()

def are_all_args_set(args):
    return args.Platform is not None and args.NAND_Config is not None

def dwSXGear(tempFolder = "temp", destFolder = "COPY_TO_SD"):
    print("--- (Skip this if you use a HWFLY modchip) ---")
    value = input("Do you want to download SX Gear? (Y/N): ")
    if value in ["s", "S", "y", "Y"]:
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
        os.path.join(tempFolder, "sigpatches{}.zip".format(dt.now().strftime("%Y%m%d%H%M%S"))),
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

def runScript(opcion, hbOpciones, sxBool):
    print(dwHekate())
    print(dwAtmosphere())
    print(dwFusee())
    print(dwSigpatches())

    if opcion in [4, 5, 6]:
        for file in os.listdir("COPY_TO_SD"):
            if file.endswith(".bin"):
                os.rename("COPY_TO_SD/" + file, "COPY_TO_SD/payload.bin")

    if sxBool:
        print("[i] Downloading SX Gear [v1.1]")
        try:
            downloadZip(
                "https://web.archive.org/web/20210128064352if_/https://sx.xecuter.com/download/SX_Gear_v1.1.zip",
                os.path.join("temp", "sxgear.zip"),
                "COPY_TO_SD",
                "SX"
            )
            print("[OK] SX Gear [v1.1] downloaded successfully.")
        except Exception as e:
            print("[!] Error downloading SX Gear [v1.1]: {}".format(e))
            print("[!] Please download it manually from https://web.archive.org/web/20210217231219/https://sx.xecuter.com/download/SX_Gear_v1.1.zip")

    if 1 in hbOpciones:
        print(dwTinfoil())
    if 2 in hbOpciones:
        print(dwGoldLeaf())
    if 3 in hbOpciones:
        print(dwAppStore())

    writeConfig(opcion, data)


if __name__ == '__main__':
    delFolder(folder = "COPY_TO_SD")
    mkFolder("temp")
    mkFolder("COPY_TO_SD")
    args = parse_args()
    if are_all_args_set(args):
        sxBool = False
        if args.NAND_Config == "1. CFW EmuNAND + OFW SysNAND":
            opcion = 1
        elif args.NAND_Config == '2. CFW EmuNAND + CFW SysNAND':
            opcion = 2
        elif args.NAND_Config == '3. CFW SysNAND':
            opcion = 3

        if args.Platform != "Erista":
            opcion = opcion + 3
            if args.Platform == "SXCore":
                sxBool = True

        hbOpciones = []
        if args.Homebrew_Apps is not None:
            for hb in args.Homebrew_Apps:
                if hb == "1. Tinfoil [may be slow to download]":
                    hbOpciones.append(1)
                elif hb == "2. HB App Store":
                    hbOpciones.append(2)
                elif hb == "3. Goldleaf":
                    hbOpciones.append(3)
        
        runScript(opcion, hbOpciones, sxBool)

        if args.Open_folder:
            print("[i] Opening COPY_TO_SD folder...")
            openFolder()
        if args.Delete_temporal_files:
            print("[i] Deleting temporal files...")
            delFolder(folder = "temp")
        