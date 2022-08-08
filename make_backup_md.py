import os
import datetime
import csv

import requests

from bs4 import BeautifulSoup

from decouple import config

import re
import time

import markdownify


credentials = config("ZENDESK_LOGIN"), config("ZENDESK_PASSWORD")
session = requests.Session()
session.auth = credentials

zendesk = config("ZENDESK_DOMAIN")
language = config("ZENDESK_LANGUAGE")

date = datetime.date.today()
backup_path = os.path.join('backups', str(date), language) + \
    '_md_only'
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

log = []


# get the articles
endpoint = zendesk + \
    '/api/v2/help_center/en-us/articles.json?sort_by=created_at&sort_order=asc'.format(
        locale=language.lower())
while endpoint:
    response = session.get(endpoint)
    if response.status_code != 200:
        print('Failed to retrieve articles with error {}'.format(
            response.status_code))
        exit()
    data = response.json()

    for article in data['articles']:
        if article['body'] is None:
            continue
        title = '# ' + article['title'] + ''
        filename = article['title'].replace(
            '/', '|') + '_{id}.md'.format(id=article['id'])
        print("processing {}".format(filename))

        article_body = article['body']

        soup = BeautifulSoup(article_body, 'html.parser')
        img_tags = soup.find_all('img')
        urls = [img['src'] for img in img_tags]

        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
            markdown = markdownify.markdownify(
                article_body, heading_style="ATX")
            f.write(title + '\n' + markdown)
        print('{id} copied!'.format(id=article['id']))

        log.append((filename, article['title'], article['author_id']))

    endpoint = data['next_page']

with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('File', 'Title', 'Author ID'))
    for article in log:
        writer.writerow(article)
