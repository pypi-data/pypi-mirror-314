import re

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
    output = ser.read_until().decode('utf-8', errors='ignore')
    match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', output)
    if match:
        return match.group(1)
    return "N/A"
