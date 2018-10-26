# Flask Web App With Selenium and Beautiful Soup
> A simple flask app integrated with selenium to run over facebook to mine data
> also using embedded twisted reactor along with gunicorn WSGI server for Heorku Usage

[![Python Version][python-image]][python-url]
[![Build Status][travis-image]][travis-url]
[![Build Status][appveyor-image]][appveyor-url]

This is a project for scrapping likers and commenters of a given post URL of facebook
It also collects the likers likings and commenters likings from their profile and store all the data
into mongo databases collections. All collected data is Publicly available by facebook. 

## Installation & Setup (Development Environment)

OS X & Linux & Windows:

```bash
git clone https://github.com/PandorAstrum/FlaskScrapper.git
pip install -r requirements.txt
```

Download (Extras):
- [Python 3.6](https://www.python.org/)
- [VS CODE](https://code.visualstudio.com/)
- [Google Chrome](https://www.google.com/chrome/?brand=CHBD&gclid=Cj0KCQjwi8fdBRCVARIsAEkDvnI_-Usd4sWPkamFkNA7G9MRls59EqPNbwY4Nu6YpvKKOQqoMw4kSV0aAqS9EALw_wcB&gclsrc=aw.ds.ds&dclid=CLrPjYCC5t0CFURnjgod4sgNdw)
- [Rabbit MQ](https://www.rabbitmq.com/install-standalone-mac.html)
- [Node js](https://nodejs.org/en/)

## Important Notes

- The settings for flask can be found on ```config.cfg``` file. Edit it to get your desired settings
- ```Binary``` folders contains all the web drivers for mac, linux and windows.
- ```backend``` folder has the flask application, ```frontend``` folder has the react application
- ```Dump``` folder only used in development on local machine to hold the uploaded file and downloaded csv file
- Before uploading the list of url for scraping in csv make sure 
all the scraping url is under same column named "URL" (header)

## Usage example (Development Environment)
##### MAC
make sure the webdriver for mac has read and write access
* Select the webdriver, then choose File > Get Info, or press Command-I.
* Click the disclosure triangle next to Sharing & Permissions to expand the section.
* Click the pop-up menu next to your user name to see the permissions settings. ...
* Change the permissions to either Read & Write or “Read only.”

N.B: Here mongo used with URI from mlab, use your own mongo environment if you change the database URL in ```config.cfg``` file

clone or download this repo
```
sudo git download https://github.com/PandorAstrum/FlaskScrapper.git
```
Open a terminal and navigate to root folder
download everything by running
```
pip install requirements.txt
npm install
```
After completion of installation run
```
npm start
```
the flask powered react would be started on ```127.0.0.0:5000```

## Helpers Library
# csv_helpers.py
> Library that helps on writing csv file and reading csv file
# generic_helpers.py
> Library that helps on various task such as get download file name or get time in provided format
# scrapper.py
> Library that helps on scrapping process

## Release History
* 1.1.0
    * Add: React as front end
    * Add: webpack to bundle all js css and image
    * Fix: Chrome browser is now headless
    * Fix: Results Tables are now more data driven
    
* 1.0.0
    * Add: flask web app Creation
    * Add: MongoDB integrations
    * Add: Selenium integrations
    * Add: helpers library for csv upload and download
    * Add: Celery with RabbitMQ added for multi threading task

## Meta

Ashiquzzaman Khan – [@dreadlordn](https://twitter.com/dreadlordn)

Distributed under the Apache License 2.0. See ``LICENSE`` for more information.

[https://github.com/PandorAstrum/FlaskScrapper](https://github.com/PandorAstrum/FlaskScrapper)

<!-- Markdown link & img dfn's -->
[python-image]: https://img.shields.io/badge/Python-3.6-yellowgreen.svg?style=flat-square
[python-url]: https://www.python.org/

[travis-image]: https://travis-ci.org/PandorAstrum/_vault.svg?branch=master
[travis-url]: https://travis-ci.org/PandorAstrum/_vault

[appveyor-image]: https://ci.appveyor.com/api/projects/status/8dxrtild5jew79pq?svg=true
[appveyor-url]: https://ci.appveyor.com/project/PandorAstrum/vault


