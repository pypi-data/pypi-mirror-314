import re

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
