# Switch2SD

Switch2SD is a Python script to download and install custom firmware, homebrew applications, and other files needed to run homebrew software on the Nintendo Switch game console.

## Dependencies
- Python 3.6 or higher
- `requests` library
- `BeautifulSoup` library

## How to use
1. Install the required dependencies.
2. Clone or download the repository to your computer.
3. Install the required dependencies by running `pip install -r requirements.txt` in the command prompt.
4. Run `python switch2sd.py` from a command prompt or terminal.
5. Follow the on-screen instructions to select the desired configuration and homebrew applications to download.
6. The files will be downloaded and extracted into a folder named `COPY_TO_SD`.
7. Copy the contents of the `COPY_TO_SD` folder to the root of your microSD card.
8. Insert the microSD card into your Nintendo Switch and enjoy your homebrew applications.

## Configuration Options
Switch2SD supports several different configuration options, depending on your Nintendo Switch model and whether or not you have a hardware modchip installed. The available options are:

- [Erista Unpatched] CFW emuNAND + OFW sysNAND
- [Erista Unpatched] CFW emuNAND + CFW sysNAND
- [Erista Unpatched] CFW sysNAND
- [SXCore & HWFly] CFW emuNAND + OFW sysNAND
- [SXCore & HWFly] CFW emuNAND + CFW sysNAND
- [SXCore & HWFly] CFW sysNAND

When you run the script, you will be prompted to select one of these options.

## Homebrew Options
Switch2SD also supports several homebrew applications that you can choose to download and install. The available options are:

- Tinfoil
- Homebrew Store
- Goldleaf

When prompted, enter the number of each homebrew application you want to download, separated by commas. If you do not want to download any of the available homebrew applications, simply press Enter without entering any numbers.

## Notes

This script was written as a proof of concept and should be used with caution. The author of this script is not responsible for any damage that may occur to your Nintendo Switch or SD card.

Thank you to all the talented developers who have contributed to the development of the Nintendo Switch homebrew scene, including those behind Fusee, Atmosphere, Hekate, Tinfoil, Goldleaf, and the Homebrew App Store. Your hard work and dedication have made it possible for gamers to enjoy a wide variety of homebrew software on their Switch consoles. We appreciate all the time and effort you've put into creating these amazing tools and applications. Keep up the great work!

Based on https://rentry.org/SwitchHackingIsEasy guides.