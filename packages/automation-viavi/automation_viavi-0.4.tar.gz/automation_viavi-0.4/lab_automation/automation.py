import serial
import time
import requests
from serial.serialutil import SerialException
import re
import glob
import json
import os
from bs4 import BeautifulSoup
def update_confluence(serial_output):

    page_ID = os.getenv('PAGE_ID'),
    api_token = os.getenv('API_TOKEN')

    content_url = f'https://conf1.ds.jdsu.net/wiki/rest/api/content/{page_ID}?expand=body.view,version'
    update_url = f'https://conf1.ds.jdsu.net/wiki/rest/api/content/{page_ID}'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(content_url, headers=headers)
    if response.status_code == 200:
        content = response.json()
        html_content = content['body']['view']['value']
        version_number = content['version']['number'] 
        soup = BeautifulSoup(html_content, 'lxml')
        table = soup.new_tag('table')
        soup.body.append(table)
        header = soup.new_tag("tr")
        table.append(header)
        for column in ["Model", "Serial Number", "MAC Address", "IP Address", "Port"]:
            th = soup.new_tag("th")
            th.string = column
            header.append(th)
        for device in serial_output:
            row = soup.new_tag("tr")
            table.append(row)
            for key in ["ProductName", "ProductSerialNumber", "ManagementEthernetMAC", "IP", "Port"]:
                td = soup.new_tag("td")
                td.string = device.get(key, "-")
                row.append(td)
        print(soup.prettify()) 
             

        updated_html_content = str(soup)

        update_payload = {
            "id": f"{page_ID}",
            "type": "page",
            "title": content['title'],
            "body": {
                "storage": {
                    "value": updated_html_content,
                    "representation": "storage"
                }
            },
            "version": {
                "number": version_number + 1
            }
        }
        

        update_response = requests.put(update_url, headers=headers, data=json.dumps(update_payload))
        
        if update_response.status_code == 200:
            print("Page updated successfully!")
        else:
            print(f"Failed to update page: {update_response.status_code}, {update_response.text}")

    else:
        print(f"Failed to fetch page content: {response.status_code}, {response.text}")
        
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

def handle_serial_response(response):
    try:
        decoded_response = response.decode('utf-8')
    except UnicodeDecodeError:
        decoded_response = response.hex()
    return decoded_response

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
def extract_symlink_and_serial(file_path):
    symlink_serial_map = {}
    rule_pattern = re.compile(r'ENV{ID_SERIAL_SHORT}=="([^"]+)",.*SYMLINK\+="([^"]+)"')
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'): 
                    continue
                match = rule_pattern.search(line)
                if match:
                    serial_number = match.group(1)
                    symlink = match.group(2)
                    symlink_serial_map[symlink] = serial_number
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to read '{file_path}'.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return symlink_serial_map


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
                        # print('Login successful')
                        return True
                    else:
                        # print('Login incorrect, retrying...')
                        ser.write(b'\n')
                        output = read_until(ser, 'login')
                        if 'login' in output.lower():
                            ser.write(b'root\n')
            # print('Login failed')
            return False
        elif '~#' in output.lower():
            # print("Already logged in")
            return True
        else:
            # print("Login prompt not found")
            return False
    except SerialException as e:
        print(f"Serial exception: {e}")
        return False
def extract_info(output):
    info = {}
    lines = output.split('\n')
    for line in lines:
        if 'ProductName' in line:
            info['ProductName'] = line.split(':')[-1].strip()
        elif 'ProductSerialNumber' in line:
            info['ProductSerialNumber'] = line.split(':')[-1].strip()
        elif 'ManagementEthernetMAC' in line:
            info['ManagementEthernetMAC'] = ':'.join(line.split(':')[-6:]).strip()
    return info

def get_ifconfig_info(ser):
    ser.write(b'ifconfig\n')
    output = read_until(ser, 'inet addr')
    match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', output)
    if match:
        return match.group(1)
    return "N/A"
def check_all_ports():
    baudrate = 115200
    serial_ports =  extract_symlink_and_serial('/etc/udev/rules.d/99-usbserial.rules')
    print(f"Found serial ports: {serial_ports}")
    devices_info = []
    for symlink, serial in serial_ports.items():
        # print(f"Attempting to connect to {port}...")
        ser,error = serial_connect("/dev/" + symlink, baudrate)
        
        if ser:
            try:
                if check_for_credentials(ser):
                    ser.write(b'\nsicutil -r -sol main\n')
                    output = read_until(ser, 'ProductName')
                    info = extract_info(output)
                    info['IP'] = get_ifconfig_info(ser)
                    info['Port'] = symlink
                    devices_info.append(info)
            
                else:
                    print(f"Failed to connect to {symlink}, {error} \n")
            finally:
                ser.close()
        else:
            print(f"Failed to connect to {symlink}, {error} \n")
    update_confluence(devices_info)  

def main():
    check_all_ports()

if __name__ == "__main__":
    main()