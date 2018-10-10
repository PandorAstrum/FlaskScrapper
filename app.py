import os
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, json
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from helpers.scrapper import login, get_driver, get_likers, get_profile_like, close, get_commenters
from helpers.generic_helpers import SCRAPE_COMPLETE,SCRAPPING_INPROGRESS, get_curr_date_time, JSONEncoder
from helpers.csv_helpers import readCSV
from helpers.generic_helpers import ListConverter


UPLOAD_FOLDER = 'C:\\Users\\Ana Ash\\Desktop\\Aldrin\\Project\\Dump'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)

app.url_map.converters['list'] = ListConverter

app.config.from_pyfile('config.cfg')  # Using the config file for setting up
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# debug: reload jinja templates
app.jinja_env.auto_reload = True

# remove cache limit (default is 50 templates)
app.jinja_env.cache = {}

# Pymongo Connections
mongo = PyMongo(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page
    :return:
    """
    _jobs_collections = mongo.db.jobs                       # get the jobs collections from mongo db
    _users_collections = mongo.db.users                     # get the users collections from mongo db

    # coming post from user page =========================
    if (request.method == "POST"):
        if (request.form.get("userprofile") == "new"):      # get if new or edit
            _os = request.form.get("MacWinNew")             # get the os
            _browser = request.form.get("browserNew")       # get the browser
            _username = request.form.get("usernameNew")     # get the username
            _password = request.form.get("passwordNew")     # get the password
            _data = {
                "user": _username,
                "pass": _password,
                "os": _os,
                "browser": _browser,
                "timeStamp": str(get_curr_date_time())
            }
            _users_collections.insert_one(_data)            # save it to mongo
        elif (request.form.get("userprofile") == "edit"):
            _selections = request.form.get("selections")    # get selection values from front end
            _get_user = _users_collections.find_one({"user": _selections})  # find matching documents from mongo
            _os = request.form.get("MacWinEdit")            # get the os
            _browser = request.form.get("browserEdit")      # get the browser
            _username = request.form.get("usernameEdit")    # get the username
            _password = request.form.get("passwordEdit")    # get the password
            _users_collections.find_one_and_update({"_id": _get_user["_id"]},
                                                   {"$set": {"user": _username,
                                                             "pass": _password,
                                                             "os": _os,
                                                             "browser": _browser}})

    _all_jobs_document = list(_jobs_collections.find())     # get all the documents from jobs collections
    _all_users_document = list(_users_collections.find())   # get all the documents from user collections
    return render_template('index.html', _job_data = _all_jobs_document, _user_data = _all_users_document)

@app.route('/userprofile', methods=['GET'])
def userprofile():
    """
    User Profile Page for adding new or edit existing
    :return:
    """
    _users_collections = mongo.db.users
    _all_users_document = list(_users_collections.find())  # get all the documents from user collections
    return render_template('user.html', _user_data = _all_users_document)

@app.route('/getuser', methods= ['GET'])
def getuser():
    """
    Route to handle Ajax call from browser
    :return:
    """
    _users_collections = mongo.db.users  # get the users collections from mongo db
    _all_users_document = list(_users_collections.find())  # get all the documents from user collections
    return jsonify(JSONEncoder().encode(_all_users_document))

@app.route('/progress', methods=['POST'])
def progress():
    """
    Progress page <all crawling mechanism starts here>
    :return:
    """
<<<<<<< HEAD
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

=======
    _jobs_collections = mongo.db.jobs                   # get the jobs collections from mongo db
    _users_collections = mongo.db.users                 # get the users collections from mongo db

    _id_list = []
    _selections = request.form.get("selections")        # get selection values from front end
    _get_user = _users_collections.find_one({"user": _selections})  # find matching documents from mongo
    _link_to_scrap = get_post()                         # list of links to scrape
    if _get_user != None:                               # error checking when document not found
        DRIVER = setup_drivers(_get_user["os"], _get_user["browser"])  # Setup the correct driver
        login(DRIVER, _get_user["user"], _get_user["pass"])  # try login to facebook
>>>>>>> 9cc9ff1b9d425989593b72880270156d2bc86442
        if DRIVER.current_url == "https://m.facebook.com/login/save-device/?login_source=login#_=_":  # login success
            for i in _link_to_scrap:
                DRIVER.get(i)                           # get the scrapping page
                _commenters_name, _commenters_profile = get_commenters(DRIVER)  # get Commenters
                _likers_name, _likers_profile = get_likers(DRIVER)  # get likers
                likers = get_profile_like(DRIVER, _likers_name, _likers_profile)  # get likers like
                commenters = get_profile_like(DRIVER, _commenters_name, _commenters_profile)  # get commenters like
                _data = {
                    "Post": i,
                    "Likers": likers,
                    "Commenters": commenters,
                    "DateStamp": str(get_curr_date_time(_strft="%b/%d/%Y %H\u002E%M"))
                }
                id_ = _jobs_collections.insert_one(_data)

                _id_list.append(id_.inserted_id)
            close(DRIVER)                               # close driver

            _job_list = []
            for j in _id_list:
                _jobs = _jobs_collections.find_one({"_id": ObjectId(j)})
                _job_list.append(_jobs)

            return render_template('results.html', _list_of_jobs = _job_list)
        else:
            close(DRIVER)
            return render_template("error.html", _error="username password combination wrong")
    else:
        return render_template("error.html", _error = f"No User profile matched with {_selections} on Database")

    # elif SCRAPE_COMPLETE:
    #     return render_template('progress.html', _progress = "Scrapping completed")

    # return render_template('progress.html', _progress = "Scrapping is in progress")

@app.route('/error', methods=['GET'])
def error():
    """
    Error page
    :return:
    """
    return render_template('error.html')

@app.route('/results/<list:_jobs_id_list>', methods=['GET'])
def results(_jobs_id_list):
    """
    Results Page specific post
    :return:
    """
    # get collections based on jobs post
    _jobs_list = []
    _jobs_collections = mongo.db.jobs
    for i in _jobs_id_list:

        _job_document = _jobs_collections.find_one({"_id": ObjectId(i)})
        _jobs_list.append(_job_document)
    # _jobs.find_one("Post")
    # global SCRAPE_COMPLETE
    # if SCRAPE_COMPLETE:
    #     # render results
    #     pass
        # return json.dumps(quotes_list)

    return render_template('results.html', _list_of_jobs = _jobs_list)

# custom methods ============================================================
def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global SCRAPE_COMPLETE
    SCRAPE_COMPLETE = True
    redirect(url_for('results'))

def setup_drivers(_os, _browser):
    """
    functions for setup the correct drivers
    :param _os: string name of os
    :param _browser: string name of browsers
    :return: driver object
    """
    if (_os == "mac"):
        if (_browser == "chrome"):
            return get_driver("mac", "chrome")
        elif (_browser == "firefox"):
            return get_driver("mac", "firefox")
        elif (_browser == "opera"):
            return get_driver("mac", "opera")
    elif (_os == "windows"):
        if (_browser == "chrome"):
            return get_driver("windows", "chrome")
        elif (_browser == "firefox"):
            return get_driver("windows", "firefox")
        elif (_browser == "opera"):
            return get_driver("windows", "opera")

def get_post():
    """
    functions to get the input scrapping post url
    :return: a list
    """
    _link = []
    if (request.form.get("postlink") == "postLink1"):
        _scrapping_link = request.form.get("singlePost")
        _processed_link = _scrapping_link.replace("www", "m")
        _link.append(_processed_link)
    elif (request.form.get("postlink") == "postLink2"):
        file = request.files['csvfile']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            _scrapping_link = readCSV(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), "URL")
            for i in _scrapping_link:
                _link.append(i.replace("www", "m"))

    return _link

@app.route("/downloadCSV", methods=["POST"])
def downloadCSV():
    def flattenjson(b, delim):
        val = {}
        for i in b.keys():
            if isinstance(b[i], dict):
                get = flattenjson(b[i], delim)
                for j in get.keys():
                    val[i + delim + j] = get[j]
            else:
                val[i] = b[i]

        return val


    if request.method == "POST":
        _data = request.json['data']
        print(_data)
        real_data = flattenjson(_data, "__")

        f = csv.writer(open("test.csv", "wb+"))
    # csv = f'No.,Likers,Their Likings,URL Links,Commenters,Thier Likings,URL Links\n'
    # for i in _var:
    #     csv = csv + i["Post"] + "\n"

        outfile = str(get_curr_date_time()) + ".csv"
        return Response(
            _data,
            mimetype="text/csv",
            headers={"Content-disposition":
                 f"attachment; filename={outfile}"})

if __name__ == '__main__':
    app.run()