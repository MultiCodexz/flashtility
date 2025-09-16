# app/src/core/flash.py
from src.utils import uart

def flash_fritzbox(uart_port):
    if uart_port:
        print(f"Flashing FritzBox via {uart_port} ...")
        # TODO: UART Flash logic implementieren
    else:
        print("Kein UART Port gefunden, kann nicht flashen.")
