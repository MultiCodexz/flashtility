#!/usr/bin/env python3
import cmd
import curses
import time
import random
import json
from pathlib import Path
import logging
import os
import serial.tools.list_ports

# -------------------------
# Logging Setup
# -------------------------
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'app.log'),
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger("Fl4zh_U17itY")

# -------------------------
# Colored / Bounce Text
# -------------------------
COLORS = [curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_YELLOW,
          curses.COLOR_BLUE, curses.COLOR_MAGENTA, curses.COLOR_CYAN, curses.COLOR_WHITE]

def println(text, bounce=False):
    def simple_print(stdscr):
        curses.start_color()
        for i, c in enumerate(COLORS):
            curses.init_pair(i + 1, c, curses.COLOR_BLACK)

        if not bounce:
            words = text.split()
            for word in words:
                color = random.choice(range(1, len(COLORS)+1))
                stdscr.addstr(word + ' ', curses.color_pair(color))
            stdscr.addstr('\n')
            stdscr.refresh()
            stdscr.getch()
        else:
            y, x = 5, 5
            direction = 1
            for char in text:
                color = random.choice(range(1, len(COLORS)+1))
                stdscr.addstr(y, x, char, curses.color_pair(color))
                stdscr.refresh()
                time.sleep(0.05)
                y += direction
                direction *= -1
                x += 1
            stdscr.getch()

    curses.wrapper(simple_print)

# -------------------------
# Config Loader
# -------------------------
CONFIG_PATH = Path(__file__).parent / "conf"
configs = {}

def load_configs():
    if not CONFIG_PATH.exists():
        os.makedirs(CONFIG_PATH)
        print(f"Ordner 'conf' erstellt: {CONFIG_PATH}")
    for file in CONFIG_PATH.glob("*.json"):
        with open(file, "r") as f:
            data = json.load(f)
            configs[file.stem] = data
            for k, v in data.items():
                globals()[k] = v
    # Ausgabe der geladenen Configs
    for name, conf in configs.items():
        println(f"Config {name}: {conf}")

    logging.info("Alle Configs geladen")

# -------------------------
# OLED Display
# -------------------------
def init_oled():
    try:
        from luma.core.interface.serial import i2c
        from luma.oled.device import ssd1306
        serial = i2c(port=1, address=0x3C)
        device = ssd1306(serial)
        device.show()
        print("OLED Display initialisiert")
        logging.info("OLED Display initialisiert")
    except Exception as e:
        print(f"Fehler OLED: {e}")
        logging.error(f"Fehler OLED: {e}")

# -------------------------
# UART Scan
# -------------------------
def init_uart_scan():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("Keine UART-Ports gefunden")
        logging.warning("Keine UART-Ports gefunden")
        return None
    for port in ports:
        print(f"Gefundener Port: {port.device}")
        logging.info(f"UART Port gefunden: {port.device}")
    # Rückgabe des ersten gefundenen Ports
    return ports[0].device

# -------------------------
# Flash Router (Platzhalter)
# -------------------------
def flash_router():
    print("Flash gestartet... (Simulation)")
    logging.info("Flash Routine gestartet")
    println("Firmware Flashing läuft...", bounce=True)

# -------------------------
# ASCII Banner
# -------------------------
def banner():
    b = """
███████╗██╗      █████╗ ████████╗███╗   ██╗██╗  ██╗
██╔════╝██║     ██╔══██╗╚══██╔══╝████╗  ██║██║ ██╔╝
█████╗  ██║     ███████║   ██║   ██╔██╗ ██║█████╔╝ 
██╔══╝  ██║     ██╔══██║   ██║   ██║╚██╗██║██╔═██╗ 
██║     ███████╗██║  ██║   ██║   ██║ ╚████║██║  ██╗
╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚═╝  ╚═╝
"""
    println(b, bounce=False)
    return "Firmware Flash Utility"

# -------------------------
# CMD Loop
# -------------------------
class Fl4zhCLI(cmd.Cmd):
    intro = banner()
    prompt = "Fl4zh_U17itY >> "

    def do_loadconfigs(self, arg):
        load_configs()

    def do_uart(self, arg):
        init_uart_scan()

    def do_flash(self, arg):
        flash_router()

    def do_oled(self, arg):
        init_oled()

    def do_exit(self, arg):
        print("Exiting...")
        return True

if __name__ == "__main__":
    Fl4zhCLI().cmdloop()
