
# My Bangumi Project



## Requirements

 - python3.10 or later
   - pywebio
   - qbittorrent-api
   - bs4 (beautifulsoup4), lxml
   - ostruct, humanize, pyyaml
   
 - BTW, we can get a requirements file in two ways:
   - `pipreqs . --encoding utf8`: generate with pipreqs tool
   - `pip freeze > requirements.txt`: use pip command, but you'd better run it in python venv


### Setup Env

 - just use run `pip install -r requirements.txt`
 - or use an venv:
   - `python3.10 -m venv env`: create a python venv
   - `. ./env/bin/activate`: active venv
   - `pip install -r requirements.txt`: install packages in venv
   - `deactivate`: to exit python venv

