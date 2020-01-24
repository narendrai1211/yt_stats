import requests
import csv
from bs4 import BeautifulSoup
filename = 'file_urls.txt'
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
        request_url = 'https://socialblade.com/youtube/'+page_type+'/'+channel_id
        social_b.append(request_url.strip())
    return social_b


def scrape_page(social):
    cnt = 1
    print(len(social))
    for request in social:
        print(request)
        data2 = requests.get(request, headers=headers)
        site_text = data2.text
        soup = BeautifulSoup(site_text, 'lxml')
        d = soup.find('div', id='YouTubeUserTopInfoBlockTop')
        channel_name = d.find('h1').text
        data_2 = d.find_all('div', class_='YouTubeUserTopInfo')
        required_form_list = [cnt, channel_name]
        for i in data_2:
            d = i.find_all('span', style="font-weight: bold;")
            for each_element in d:
                required_form = each_element.text.replace(',', '')
                required_form_list.append(required_form)
        print(required_form_list)
        main_list.append(required_form_list)
        cnt += 1
    return main_list


def check_length(contents, header):
    for i in contents:
        if len(i) == len(header):
            return 0
        else:
            print('Column Mis-match cannot write data')
            return 1


def write_to_file(contents):
    print(contents)
    list_header = ['Sr.No.', 'Channel Name', 'Uploads', 'Subscribers', 'Views', 'Country_Code', 'Channel_Type','Created_Date']
    d = check_length(contents, list_header)
    if d == 1:
        print('Cannot Write Data')

    else:
        print('Writing Data')
        with open('yt_stats.csv', 'w') as file:
            csv_writer_inside = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar=' ')
            csv_writer_inside.writerow(list_header)
            csv_writer_inside.writerows(main_list)
        print('Written Data')


def main_program():
    data = read_file(filename)
    req_urls = generate_required_url(data)
    content = scrape_page(req_urls)
    write_to_file(content)


main_program()
