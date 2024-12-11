from .serial_utils import check_all_ports
import os

def main():
    print("Starting automation process\n")
    check_all_ports()
    page_ID = os.getenv('PAGE_ID')
    api_token = os.getenv('API_TOKEN')
    print(page_ID, api_token)

if __name__ == "__main__":
    main()