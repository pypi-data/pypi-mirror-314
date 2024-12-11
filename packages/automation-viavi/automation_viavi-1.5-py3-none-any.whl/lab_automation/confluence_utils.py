import requests
from bs4 import BeautifulSoup
import json
import os

def update_confluence(serial_output):
    page_ID = os.getenv('PAGE_ID')
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
