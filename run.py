from facebook_data_scraper import *
from settings import *
from pages import PAGE_LINKS
import json


def write_data(raw_data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(raw_data, file)
    print('Data have saved in JSON format...')


def main():
    login(EMAIL, PASSWORD)
    raw_data = extract_data(PAGE_LINKS, numOfScroll=numOfScroll, grab_comment=grab_comment)
    write_data(raw_data)

if __name__ == "__main__":
    main()
