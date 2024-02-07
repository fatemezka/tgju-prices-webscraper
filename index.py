from bs4 import BeautifulSoup
import requests
import csv
import re

tgju_url = "https://www.tgju.org/"

info_list = []

response = requests.get(tgju_url)
if response.status_code == 200:
    result = BeautifulSoup(response.text, "html.parser")

    container_div = result.find("div", class_="container")
    info_ul = container_div.find("ul", class_="info-bar mobile-hide")
    li_tags = info_ul.find_all("li")

    counter = 1
    for li in li_tags:
        h3 = li.find('h3')
        span_price = li.find('span', class_='info-price')
        span_change = li.find('span', class_='info-change')
        change_status = li["class"]
        page_path = re.search(
            r"window\.location='(.*?)'",
            li['onclick']
        ).group(1)

        name = h3.text.strip()
        profile_link = tgju_url + page_path
        price = span_price.text.strip()
        change = span_change.text.strip()
        status = change_status[0]

        info_list.append({
            "Counter": counter,
            "Name": name,
            "ProfileLink": profile_link,
            "Price": price,
            "Change": change,
            "Status": status
        })
        counter += 1


if len(info_list) != 0:
    header = ['Counter', 'Name', 'ProfileLink', 'Price', 'Change', 'Status']
    filename = 'info_list.csv'

    try:
        # Write data to CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)

            writer.writeheader()

            for item in info_list:
                writer.writerow(item)
        print(f"These information saved in {filename} successfully.")
    except Exception as e:
        print("An error occurred:", e)


# print(info_list)
