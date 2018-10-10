import os
from bson import ObjectId
from celery import Celery
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, json
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from helpers.scrapper import login, get_driver, get_likers, get_profile_like, close, get_commenters
from helpers.generic_helpers import SCRAPE_COMPLETE,SCRAPPING_INPROGRESS, get_curr_date_time, JSONEncoder
from helpers.csv_helpers import readCSV
from helpers.generic_helpers import ListConverter


ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)

# debug: reload jinja templates
app.jinja_env.auto_reload = True

# remove cache limit (default is 50 templates)
app.jinja_env.cache = {}

# custom list mapper for routes
app.url_map.converters['list'] = ListConverter

app.config.from_pyfile('config.cfg')  # Using the config file for setting up

# Pymongo Connections
mongo = PyMongo(app)

# celery connections
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])



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


@app.route('/status/<task_id>')
def taskstatus(task_id):
    _task = scrapping_task.AsyncResult(task_id)
    if _task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': _task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif _task.state != 'FAILURE':
        response = {
            'state': _task.state,
            'current': _task.info.get('current', 0),
            'total': _task.info.get('total', 1),
            'status': _task.info.get('status', '')
        }
        if 'result' in _task.info:
            response['result'] = _task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': _task.state,
            'current': 1,
            'total': 1,
            'status': str(_task.info),  # this is the exception raised
        }
    return jsonify(response)

@app.route('/progress', methods=['POST'])
def progress():
    """
    Progress page <all crawling mechanism starts here>
    :return:
    """
    _selections = request.form.get('selections')
    _activeLink = request.form.get("postlink")
    _scrap_link = get_post(_activeLink)

    _task = scrapping_task.apply_async(args=[_selections, _scrap_link])

    return render_template('progress.html', _post=_scrap_link, _task = _task.id)


    # return render_template('progress.html')

    #
    #         for i in _link_to_scrap:


    #                                       # close driver
    #
    #         _job_list = []
    #         for j in _id_list:
    #             _jobs = _jobs_collections.find_one({"_id": ObjectId(j)})
    #             _job_list.append(_jobs)
    #
    #         return render_template('results.html', _list_of_jobs = _job_list)
    #     else:
    #         close(DRIVER)
    #         return render_template("error.html", _error="username password combination wrong")
    # else:
    #     return render_template("error.html", _error = f"No User profile matched with {_selections} on Database")

    # elif SCRAPE_COMPLETE:
    #     return render_template('progress.html', _progress = "Scrapping completed")

    # return render_template('progress.html', _progress = "Scrapping is in progress")

@celery.task(bind=True)
def scrapping_task(self, _user, _scrapLink):
    _jobs_collections = mongo.db.jobs  # get the jobs collections from mongo db
    _users_collections = mongo.db.users  # get the users collections from mongo db
    _id_list = []
    _get_user = _users_collections.find_one({"user": _user})  # find matching documents from mongo
    _total = 100
    if _get_user != None:  # error checking when document not found
        DRIVER = setup_drivers(_get_user["os"], _get_user["browser"])  # Setup the correct driver
        login(DRIVER, _get_user["user"], _get_user["pass"])  # try login to facebook
>>>>>>> 9cc9ff1b9d425989593b72880270156d2bc86442
        if DRIVER.current_url == "https://m.facebook.com/login/save-device/?login_source=login#_=_":  # login success
            self.update_state(state='Logging in..',
                              meta={'current': 5, 'total': _total,
                                    'status': 200})
            for i in _scrapLink:
                DRIVER.get(i)                           # get the scrapping page
                self.update_state(state=f'Getting URL {i}',
                                  meta={'current': 10, 'total': _total,
                                        'status': 200})

                _commenters_name, _commenters_profile = get_commenters(DRIVER)  # get Commenters

                self.update_state(state='Getting commenters',
                                  meta={'current': 15, 'total': _total,
                                        'status': 200})
                _likers_name, _likers_profile = get_likers(DRIVER)  # get likers

                self.update_state(state='Getting likers',
                                  meta={'current': 20, 'total': _total,
                                        'status': 200})
                likers = get_profile_like(DRIVER, _likers_name, _likers_profile)  # get likers like
                self.update_state(state='Getting Likers profile likes',
                                  meta={'current': 50, 'total': _total,
                                        'status': 200})
                commenters = get_profile_like(DRIVER, _commenters_name, _commenters_profile)  # get commenters like
                self.update_state(state='Getting commenters profile likes',
                                  meta={'current': 80, 'total': _total,
                                        'status': 200})
                _data = {
                    "Post": i,
                    "Likers": likers,
                    "Commenters": commenters,
                    "DateStamp": str(get_curr_date_time(_strft="%b/%d/%Y %H\u002E%M"))
                }
                self.update_state(state='Inserting data into mongo',
                                  meta={'current': 95, 'total': _total,
                                        'status': 200})
                id_ = _jobs_collections.insert_one(_data)

                _id_list.append(JSONEncoder().encode(id_.inserted_id))

            close(DRIVER)
    return {'current': 100, 'total': _total, 'status': 'Scrape Complete',
            'result': _id_list}











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

def get_post(_activePost):
    """
    functions to get the input scrapping post url
    :return: a list
    """
    _link = []
    if (_activePost == "postLink1"):
        _scrapping_link = request.form.get("singlePost")
        _processed_link = _scrapping_link.replace("www", "m")
        _link.append(_processed_link)
    elif (_activePost == "postLink2"):
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

        real_data = flattenjson(_data, "__")
        print(json.loads(_data))
        print(real_data)

        outfile = str(get_curr_date_time()) + ".csv"
        # return Response(
        #     csv,
        #     mimetype="text/csv",
        #     headers={"Content-disposition":
        #          f"attachment; filename={outfile}"})

# celery tasks ======================================================


@celery.task(bind=True)
def scrape_likers(self):
    pass
@celery.task(bind=True)
def scrape_commenters(self):
    pass
@celery.task(bind=True)
def scrape_profile_likes(self):
    pass
@celery.task(bind=True)
def dumping_data_into_mongo(self):
    pass

if __name__ == '__main__':
    app.run()