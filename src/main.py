# src/main.py
import sys
import os
import cmd

# ─────────── Pfad für eigene Module hinzufügen ───────────
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ─────────── Eigene Module importieren ───────────
from utils import colored, config_loader, logger
from modules import flash, oled, uart

# ─────────── Banner-Funktion ───────────
def banner():
    text = "Firmware Flash Utility"
    colored.println(text, bounce=True)  # animiert / rainbow
    return ""

# ─────────── CMD-Loop ───────────
class FirmwareCLI(cmd.Cmd):
    intro = banner()
    prompt = "Fl4zh_U17itY >> "

    def __init__(self):
        super().__init__()
        self.configs = config_loader.load_configs()  # lädt alle conf/*.json
        self.oled = None
        self.uart_port = None

    def do_oled(self, arg):
        "Initialisiert das OLED Display"
        self.oled = oled.init_oled()
        print("OLED Display initialized.")

    def do_uart(self, arg):
        "Scannt und setzt den UART Port"
        self.uart_port = uart.scan_uart()
        if self.uart_port:
            print(f"UART Port gesetzt: {self.uart_port}")
        else:
            print("[!] Kein UART Port gefunden.")

    def do_flash(self, arg):
        "Führt den Firmware Flash aus"
        flash.flash_fritzbox(self.uart_port)

    def do_exit(self, arg):
        "Beendet das Programm"
        print("Bye!")
        return True

# ─────────── Entry Point ───────────
if __name__ == "__main__":
    FirmwareCLI().cmdloop()
