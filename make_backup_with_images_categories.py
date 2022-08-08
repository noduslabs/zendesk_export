import os
import datetime
import csv

import requests

from bs4 import BeautifulSoup

from decouple import config

import re
import time


credentials = config("ZENDESK_LOGIN"), config("ZENDESK_PASSWORD")
session = requests.Session()
session.auth = credentials

zendesk = config("ZENDESK_DOMAIN")
language = config("ZENDESK_LANGUAGE")

date = datetime.date.today()
backup_path = os.path.join(str(date), language) + \
    '_with_images_by_category_names'
if not os.path.exists(backup_path):
    os.makedirs(backup_path)

log = []

# get categories
category_endpoint = zendesk + \
    '/api/v2/help_center/en-us/sections'.format(
        locale=language.lower())

category_response = session.get(category_endpoint)
if category_response.status_code != 200:
    print('Failed to retrieve articles with error {}'.format(
        category_response.status_code))
    exit()
category_data = category_response.json()

sections = {}
for section in category_data['sections']:
    sections[section['id']] = section['name']


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
        title = '<h1>' + article['title'] + '</h1>'
        filename = '{id}.html'.format(id=article['id'])
        print("processing {}".format(filename))

        article_body = article['body']

        category_id = article['section_id']
        category = sections[category_id]

        soup = BeautifulSoup(article_body, 'html.parser')
        img_tags = soup.find_all('img')
        urls = [img['src'] for img in img_tags]

        if not os.path.exists(backup_path + '/' + str(category)):
            os.makedirs(backup_path + '/' + str(category))

        for url in urls:
            img_filename = format(url).split("/")[-1]
            if not img_filename:
                print("Regex didn't match with the url: {}".format(url))
                continue
            with open(os.path.join(backup_path, str(category), img_filename), 'wb') as f:
                if 'http' not in url:
                    # sometimes an image source can be relative
                    # if it is provide the base url which also happens
                    # to be the site variable atm.
                    url = '{}{}'.format(zendesk, url)
                print("trying to get {}".format(url))
                try:
                    response = requests.get(url)
                    f.write(response.content)
                    article_body = article_body.replace(
                        str(url), str(img_filename))
                    print("saved image {}".format(img_filename))
                    log.append(
                        (img_filename, article['title'], article['author_id']))
                except:
                    print('could not get {}'.format(url))
                    log.append(
                        ('could not get {}'.format(url)))
                    pass

        with open(os.path.join(backup_path, str(category), filename), mode='w', encoding='utf-8') as f:
            f.write(title + '\n' + article_body)
        print('{id} copied!'.format(id=article['id']))

        log.append((filename, article['title'], article['author_id']))

    endpoint = data['next_page']

with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(('File', 'Title', 'Author ID'))
    for article in log:
        writer.writerow(article)
