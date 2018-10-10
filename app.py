import datetime

from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, after_this_request
from flask_pymongo import PyMongo
from helpers.scrapper import login, get_driver, get_likers, get_profile_like, close, get_commenters
from helpers.generic_helpers import SCRAPE_COMPLETE,SCRAPPING_INPROGRESS, get_curr_date_time

app = Flask(__name__)

app.config.from_pyfile('config.cfg')  # Using the config file for setting up

ALLOWED_EXTENSIONS = set(['csv'])
# debug: reload jinja templates
app.jinja_env.auto_reload = True

# remove cache limit (default is 50 templates)
app.jinja_env.cache = {}

# Pymongo Connections
mongoConnections = PyMongo(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    """
    Home page
    :return:
    """
    _jobs = mongoConnections.db.jobs    # get the jobs collections from mongo db
    _all_collections = list(_jobs.find()) # get all the documents from the collections
    return render_template('index.html', _data = _all_collections)  # render index page with collections list

@app.route('/progress', methods=['POST'])
def progress():
    """
    Progress page <all crawling mechanism starts here>
    :return:
    """
    global SCRAPE_COMPLETE
    global SCRAPPING_INPROGRESS
    if not SCRAPPING_INPROGRESS:
        SCRAPPING_INPROGRESS = True
        # global LIKERS_NAME
        # start the crawler and execute a callback when complete
        # eventual = crawl_runner.crawl(FacebookSpider(base_url=["https://www.facebook.com/5min.crafts/videos/286999302029750/"]))
        # eventual.addCallback(finished_scrape)

        # SETUP the Correct driver

        if (request.form.get("MacWin") == "mac"):
            if (request.form.get("browser") == "chrome"):
                DRIVER = get_driver("mac", "chrome")
            elif (request.form.get("browser") == "firefox"):
                DRIVER = get_driver("mac", "firefox")
            elif (request.form.get("browser") == "opera"):
                DRIVER = get_driver("mac", "opera")

        elif (request.form.get("MacWin") == "windows"):
            if (request.form.get("browser") == "chrome"):
                DRIVER = get_driver("windows", "chrome")
            elif (request.form.get("browser") == "firefox"):
                DRIVER = get_driver("windows", "firefox")
            elif (request.form.get("browser") == "opera"):
                DRIVER = get_driver("windows", "opera")
        
        elif (request.form.get("MacWin") == "linux"):
            if (request.form.get("browser") == "chrome"):
                DRIVER = get_driver("linux", "chrome")
            elif (request.form.get("browser") == "firefox"):
                DRIVER = get_driver("linux", "firefox")
            elif (request.form.get("browser") == "opera"):
                DRIVER = get_driver("linux", "opera")

        _username = request.form.get("username")
        _password = request.form.get("password")
        # try login to facebook using request

        login(DRIVER, _username, _password)

        if DRIVER.current_url == "https://m.facebook.com/login/save-device/?login_source=login#_=_":  # login success
            if (request.form.get("postlink") == "postLink1"):
                scrapping_link = request.form.get("singlePost")
                processed_link = scrapping_link.replace("www", "m")
                DRIVER.get(processed_link)

                # get commenters
                _commenters_name, _commenters_profile = get_commenters(DRIVER)  # get Commenters
                # get likers
                _likers_name, _likers_profile = get_likers(DRIVER)  # get likers
                likers = get_profile_like(DRIVER, _likers_name, _likers_profile)    # get likers like
                commenters = get_profile_like(DRIVER, _commenters_name, _commenters_profile)    # get commenters like

                close(DRIVER)

                # process dot
                # \u002E

                _jobs = mongoConnections.db.jobs
                id_ = _jobs.insert({
                    "Post" : scrapping_link,
                    "Likers" : likers,
                    "Commenters" : commenters,
                    "DateStamp" : str(get_curr_date_time(_strft="%b/%d/%Y %H\u002E%M"))
                })
                # get the data again
                _get_collections = _jobs.find_one({"_id": ObjectId(id_)})

                return render_template('results.html',
                                        _likes=_get_collections["Likers"],
                                        _comments = _get_collections["Commenters"],
                                        _post_link=_get_collections["Post"])
            elif (request.form.get("postlink") == "postLink2"):
                pass
            else:
                return render_template("error.html", _data = "Invalid combination of username and password")

        return render_template('progress.html', _progress = "Scrapping started")
    elif SCRAPE_COMPLETE:
        return render_template('progress.html', _progress = "Scrapping completed")

    return render_template('progress.html', _progress = "Scrapping is in progress")


@app.route('/error', methods=['GET', 'POST'])
def error():
    """
    Error page
    :return:
    """
    return render_template('error.html')

@app.route('/results/<_jobs_id>', methods=['GET'])
def results(_jobs_id):
    """
    Results Page <render all results here>
    :return:
    """
    # get collections based on jobs post
    _jobs = mongoConnections.db.jobs
    _get_collections = _jobs.find_one({"_id" : ObjectId(_jobs_id)})



    # _jobs.find_one("Post")
    # global SCRAPE_COMPLETE
    # if SCRAPE_COMPLETE:
    #     # render results
    #     pass
        # return json.dumps(quotes_list)

    return render_template('results.html',
                           _likes = _get_collections["Likers"],
                           _comments = _get_collections["Commenters"],
                           _post_link = _get_collections["Post"])


def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global SCRAPE_COMPLETE
    SCRAPE_COMPLETE = True
    redirect(url_for('results'))

if __name__ == '__main__':
    app.run()


