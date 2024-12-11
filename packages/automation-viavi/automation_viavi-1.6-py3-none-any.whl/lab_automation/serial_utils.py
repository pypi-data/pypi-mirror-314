import serial
from serial.serialutil import SerialException
import time
from .device_info_extractor import extract_info, get_ifconfig_info
from .confluence_utils import update_confluence
from .udev_parser import extract_symlink_and_serial

def serial_connect(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate, timeout=2)
        if ser.is_open:
            print(f"Connected to {port} at {baudrate} baud")
        else:
            ser.open()
        return ser, None
    except serial.SerialException as e:
        print(f"Failed to open port {port}: {e}")
        return None, str(e)

def read_until(ser, expected_prompt, timeout=5):
    buffer = ""
    ser.timeout = 0.5
    end_time = time.time() + timeout
    while time.time() < end_time:
        if ser.in_waiting > 0:
            buffer += ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
            if expected_prompt in buffer.lower():
                return buffer
    return buffer

def check_for_credentials(ser):
    try:
        ser.write(b'\n')
        output = read_until(ser, 'login')
        if 'login' in output.lower():
            ser.write(b'root\n')
            passwords = ['SiG2018\n', '5m8t0s0\n']
            for password in passwords:
                output = read_until(ser, 'password')
                if 'password' in output.lower():
                    ser.write(f'{password}'.encode())
                    output = read_until(ser, 'root@')
                    if 'login incorrect' not in output.lower():
                        return True
                    else:
                        ser.write(b'\n')
                        output = read_until(ser, 'login')
                        if 'login' in output.lower():
                            ser.write(b'root\n')
            return False
        elif '~#' in output.lower():
            return True
        else:
            return False
    except SerialException as e:
        print(f"Serial exception: {e}")
        return False

def check_all_ports():
    baudrate = 115200
    serial_ports = extract_symlink_and_serial('/etc/udev/rules.d/99-usbserial.rules')
    print(f"Found serial ports: {serial_ports}")
    devices_info = []
    for symlink, serial in serial_ports.items():
        ser, error = serial_connect(f"/dev/{symlink}", baudrate)
        if ser:
            try:
                if check_for_credentials(ser):
                    ser.write(b'\nsicutil -r -sol main\n')
                    output = read_until(ser, 'ProductName')
                    info = extract_info(output)
                    info['IP'] = get_ifconfig_info(ser)
                    info['Port'] = symlink
                    devices_info.append(info)
            finally:
                ser.close()
        else:
            print(f"Failed to connect to {symlink}, {error}")
    if serial_ports:
        update_confluence(devices_info)
