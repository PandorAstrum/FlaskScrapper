# Flask Web App With Scrapy Framework
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

Configure the settings for flask can be found on ```config.cfg``` file. Edit it to get your desired settings

```Binary``` folders contains all the web drivers for both mac and windows.

## Usage example (Development Environment)

To run the flask project:

navigate to the root folder
```
python app.py
```

## Helpers Library
# csv_helpers.py
> Library that helps on writing csv file and reading csv file
# db_helpers.py
> Library that helps on communicating with mongo db
# generic_helpers.py
> Library that helps on various task such as get download file name or get time in provided format
# scrapper.py
> Library that helps on scrapping process

## Release History

* 1.0.0
    * Add: flask web app
    * Add: MongoDB integrations
    * Add: Scrapy framework integrations
    * Add: helpers library

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


