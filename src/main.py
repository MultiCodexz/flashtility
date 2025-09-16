# app/src/main.py
import cmd
import utils.config_loader as config_loader
import utils.colored as colored
import modules.oled as oled_display
import modules.flash as flash
import modules.uart as uart
from utils.colored import *
from utils.config_loader import *
from utils.logger import *
from modules.oled import *
from modules.flash import * 
from modules.uart import * 


def banner():
    text = "Firmware Flash Utility"
    colored.println(text, bounce=True)
    return ""

class FirmwareCLI(cmd.Cmd):
    intro = banner()
    prompt = "Fl4zh_U17itY >> "
    
    def __init__(self):
        super().__init__()
        self.configs = config_loader.load_configs()
        self.oled = None
        self.uart_port = None

    def do_oled(self, arg):
        "Initialisiert das OLED Display"
        self.oled = oled_display.init_oled()
        print("OLED Display initialized.")

    def do_uart(self, arg):
        "Scannt und setzt den UART Port"
        self.uart_port = uart.scan_uart()
        if self.uart_port:
            print(f"UART Port gesetzt: {self.uart_port}")

    def do_flash(self, arg):
        "Führt den Firmware Flash aus"
        flash.flash_fritzbox(self.uart_port)

    def do_exit(self, arg):
        "Beendet das Programm"
        print("Bye!")
        return True

if __name__ == "__main__":
    FirmwareCLI().cmdloop()
