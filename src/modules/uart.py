# app/src/utils/uart.py
import serial.tools.list_ports
from src.utils import logger

def scan_uart():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        logger.log_info(f"Detected UART: {p.device}")
        print(f"Detected UART: {p.device}")
    if ports:
        return ports[0].device
    return None
