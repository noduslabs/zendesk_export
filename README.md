# Export Zendesk Knowledge Base

Using this python script, you can export your Zendesk knowledge base.

You can later use software like [InfraNodus](https://infranodus.com) to analyze this knowledge base and to find the main topics inside, see how the different pages are connected, etc.

All the data gets saved into `/backups/` folder with today's date, e.g. `/backups/2022-08-08`

Inside this folder you have different folders depending on the type of export option you chose below.

Several export options are available:

1. Backup all the articles as html

`make_backup_articles_only.py`

2. Backup all the articles with the images used in them as html
   
`make_backup_with_images.py`

3. Backup all the articles with the images used in them, separate by folders that reflect the sections used in your Zendesk
   
`make_backup_with_images_categories.py`

4. Backup all your Zendesk knowledge base articles in the markdown (MD) format, separated by categories

`make_backup_with_images_categories_md.py`

5. Backup all your Zendesk knowledge base articles in the markdown (MD) format, saved into one folder (good for later analysis with [InfraNodus](https://infranodus.com))

`make_backup_md.py`


## To Run

1. Clone the repo
2. Install dependencies listed in `requirements.txt`
3. Rename the `.env.sample` file to `.env` 
4. Add your Zendesk credentials to the `.env` file
5. Launch the script (e.g. `python3 make_backup_with_images_categories.py`)

## Advanced Help

To install the dependencies listed in the `requirements.txt` file:

```
pip3 install -r requirements.txt
```

For listing all the dependencies in the `requirements.txt` file:

```
pipreqs --force
```

## To-Do

[ ] Add links between pages