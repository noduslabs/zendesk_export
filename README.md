# Export Zendesk Knowledge Base

Using this python script, you can export your Zendesk knowledge base.

Several options are available:

1. Backup all the articles

`make_backup_articles_only.py`

2. Backup all the articles with the images used in them
   
`make_backup_with_images.py`

3. Backup all the articles with the images used in them, separate by folders that reflect the sections used in your Zendesk
   
`make_backup_with_images_categories.py`

## To Run

1. Clone the repo
2. Install dependencies listed in `requirements.txt`
3. Rename the `.env.sample` file to `.env` 
4. Add your Zendesk credentials to the `.env` file
5. Launch the script (e.g. `python3 make_backup_with_images_categories.py`)

