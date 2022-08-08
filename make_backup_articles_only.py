from decouple import config
import os
import datetime
import csv

import requests


credentials = config("ZENDESK_LOGIN"), config("ZENDESK_PASSWORD")
session = requests.Session()
session.auth = credentials


zendesk = config("ZENDESK_DOMAIN")
language = config("ZENDESK_LANGUAGE")

date = datetime.date.today()
backup_path = os.path.join(str(date), language)
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

log = []

endpoint = zendesk + \
    '/api/v2/help_center/en-us/articles.json'.format(locale=language.lower())
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
        title = '<h1>' + article['title'] + '</h1>'
        filename = '{id}.html'.format(id=article['id'])
        with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
            f.write(title + '\n' + article['body'])
        print('{id} copied!'.format(id=article['id']))

        log.append((filename, article['title'], article['author_id']))

    endpoint = data['next_page']

with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('File', 'Title', 'Author ID'))
    for article in log:
        writer.writerow(article)
