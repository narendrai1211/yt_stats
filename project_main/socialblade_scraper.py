import requests
import csv
from bs4 import BeautifulSoup
filename = 'file_urls.txt'
csv_body = []
main_list = []
social_b = []
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
}


def read_file(fname):
    with open(fname, 'r') as f:
        data = f.readlines()
    return data


def generate_required_url(data):
    for i_each in data:
        page_type = i_each.split('/')[-2]
        channel_id = i_each.split('/')[-1]
        print(channel_id)
        print(page_type)
        request_url = 'https://socialblade.com/youtube/'+page_type+'/'+channel_id
        social_b.append(request_url.strip())
    return social_b


def scrape_page(social):
    for request in social:
        data2 = requests.get(request, headers=headers)
        site_text = data2.text
        soup = BeautifulSoup(site_text, 'lxml')
        d = soup.find('div', id='YouTubeUserTopInfoBlockTop')
        data_2 = d.find_all('div', class_='YouTubeUserTopInfo')
        csv_body.clear()
        for i in data_2:
            d = i.find_all('span', style="font-weight: bold;")
            for i_data in d:
                required_form = i_data.text.replace(',', '')
                csv_body.append(required_form)
        main_list.append(csv_body)
    return main_list


def write_to_file(contents):
    list_header = ['Uploads', 'Subscribers', 'Views', 'Country_Code', 'Channel_Type','Created_Date']
    with open('yt_stats.csv', 'w') as file:
        csv_writer_inside = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar=' ')
        csv_writer_inside.writerow(list_header)
        csv_writer_inside.writerows(contents)


def main_program():
    data = read_file(filename)
    req_urls = generate_required_url(data)
    content = scrape_page(req_urls)
    write_to_file(content)


main_program()
