import os
from bson import ObjectId
from celery import Celery
from flask import Flask, render_template, request, redirect, url_for, jsonify, json
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from helpers.scrapper import login, get_driver, get_likers, get_profile_like, close, get_commenters
from helpers.generic_helpers import SCRAPE_COMPLETE,SCRAPPING_INPROGRESS, get_curr_date_time, JSONEncoder, allowed_file
from helpers.csv_helpers import readCSV
from helpers.generic_helpers import ListConverter

app = Flask(__name__)                                       # the flask app initialization
app.jinja_env.auto_reload = True                            # debug: reload jinja templates
app.jinja_env.cache = {}                                    # remove cache limit (default is 50 templates)
app.url_map.converters['list'] = ListConverter              # custom list mapper for routes
app.config.from_pyfile('config.cfg')                        # Using the config file for setting up

mongo = PyMongo(app)                                        # Pymongo Connections
celery = Celery(app.name,
                broker=app.config['CELERY_BROKER_URL'],
                backend=app.config['CELERY_RESULT_BACKEND'], include=['scrapping_task'])  # celery connections


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Home page
    :return:
    """
    _jobs_collections = mongo.db.jobs                       # get the jobs collections from mongo db
    _users_collections = mongo.db.users                     # get the users collections from mongo db

    # coming post from user page =========================
    if request.method == "POST":
        if request.form.get("userprofile") == "new":        # get if new or edit
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
        elif request.form.get("userprofile") == "edit":
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
    return render_template('index.html', _job_data=_all_jobs_document, _user_data=_all_users_document)


@app.route('/userprofile', methods=['GET'])
def userprofile():
    """
    User Profile Page for adding new or edit existing
    :return:
    """
    _users_collections = mongo.db.users
    _all_users_document = list(_users_collections.find())           # get all the documents from user collections
    return render_template('user.html', _user_data=_all_users_document)


@app.route('/getuser', methods=['GET'])
def getuser():
    """
    Route to handle Ajax call from browser
    :return:
    """
    _users_collections = mongo.db.users                             # get the users collections from mongo db
    _all_users_document = list(_users_collections.find())           # get all the documents from user collections
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
    _idvalue = request.form.get('idvalue')          # get the id of the user
    _timeout = float(request.form.get('rangeslider'))# get the slider value for timeout
    _activeLink = request.form.get("postlink")      # get the active post selections single / multiple
    _scrap_link = get_post(_activeLink)             # actions perform based on post selections

    if _idvalue != "None":
        _task = scrapping_task.apply_async(args=[_idvalue, _timeout, _scrap_link]) # start celery task in another thread

        return render_template('progress.html', _post=_scrap_link, _task=_task.id)
    else:
        return render_template('error.html', _error="No User selected")


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

    return render_template('results.html', _list_of_jobs=_jobs_list)


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


# custom methods ============================================================

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


# celery tasks ======================================================
@celery.task(bind=True)
def scrapping_task(self, _idvalue, _timeout,  _scrapLink):
    _likes_profile_likes = {}
    _comments_profile_likes = {}
    _likers_like = []
    _likers_like_url = []

    _jobs_collections = mongo.db.jobs  # get the jobs collections from mongo db
    _users_collections = mongo.db.users  # get the users collections from mongo db
    _id_list = []
    _get_user = _users_collections.find_one({"_id": ObjectId(_idvalue)})  # find matching documents from
    _total = 100
    if _get_user != None:  # error checking when document not found
        DRIVER = get_driver(_get_user["os"], _get_user["browser"])  # Setup the correct driver
        login(DRIVER, _timeout, _get_user["user"], _get_user["pass"])  # try login to facebook
        if DRIVER.current_url == "https://m.facebook.com/login/save-device/?login_source=login#_=_":  # login success
            self.update_state(state='Logging in..',
                              meta={'current': 5, 'total': _total,
                                    'status': 200})
            for i in _scrapLink:
                DRIVER.get(i)                           # get the scrapping page
                self.update_state(state=f'Getting URL {i}',
                                  meta={'current': 10, 'total': _total,
                                        'status': 200})

                _commenters_names, _commenters_profiles = get_commenters(DRIVER, _timeout)  # get Commenters

                self.update_state(state='Getting commenters',
                                  meta={'current': 15, 'total': _total,
                                        'status': 200})
                _likers_names, _likers_profiles = get_likers(DRIVER, _timeout)  # get likers

                _data = {
                    "Post": i.replace('https://m.', 'https://www.'),
                    "Likers": _likes_profile_likes,
                    "Commenters": _comments_profile_likes,
                    "DateStamp": str(get_curr_date_time(_strft="%b/%d/%Y %H\u002E%M"))
                }
                self.update_state(state='Inserting data into mongo',
                                  meta={'current': 95, 'total': _total,
                                        'status': 200})
                id_ = _jobs_collections.insert_one(_data)

                # for loop on likers profile
                _likers_iterator = 0
                for _liker_profile in _likers_profiles:
                    current_like_name = _likers_names[_likers_iterator]
                    get_profile_like(DRIVER, _timeout, _likes_profile_likes, current_like_name, _liker_profile)
                    _jobs_collections.find_one_and_update({"_id": ObjectId(id_.inserted_id)},
                                                          {"$set": {"Likers": _likes_profile_likes}})
                    _likers_iterator += 1

                _commenters_iterator = 0
                for _commenter_profile in _commenters_profiles:
                    current_comment_name = _commenters_names[_commenters_iterator]
                    get_profile_like(DRIVER, _timeout, _comments_profile_likes, current_comment_name, _commenter_profile)
                    _jobs_collections.find_one_and_update({"_id": ObjectId(id_.inserted_id)},
                                                          {"$set": {"Likers": _comments_profile_likes}})
                    _commenters_iterator += 1

                _id_list.append(JSONEncoder().encode(id_.inserted_id))
                # self.update_state(state='Getting likers',
                #                   meta={'current': 20, 'total': _total,
                #                         'status': 200})


            close(DRIVER)
    return {'current': 100, 'total': _total, 'status': 'Scrape Complete',
            'result': _id_list}


if __name__ == '__main__':
    app.run()