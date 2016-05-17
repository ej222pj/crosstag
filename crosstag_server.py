# -*- coding: utf-8 -*-
import json
import smtplib
import bcrypt
from datetime import datetime, timedelta
from optparse import OptionParser
import config as cfg
from flask import request
from crosstag_init import app, db, jsonify, render_template, flash, redirect, Response, session
from db_service import register_login_sql_client as registration_client
from db_service import users_sql_client as user_client
from db_service import debt_sql_client as debt_client
from db_service import update_tenant_information_sql_client as update_tenant_client
from db_service import tagevents_sql_client as tag_client
from db_models import debt
from db_models import detailedtagevent
from db_models import tagevent
from db_models import user
from db_models import sql_user
from db_models import sql_debt
from db_models import sql_tagevent
from forms.edit_user import EditUser
from forms.new_debt import NewDebt
from forms.new_tag import NewTag
from forms.new_user import NewUser
from forms.search_user import SearchUser
from forms.login import Login
from forms.registration import Register
from forms.edit_tenant import EditTenant
from forms.edit_general_information import EditGeneralInformation
from forms.edit_fortnox_information import EditFortnoxInformation
from fortnox.fortnox import Fortnox
from server_helper_scripts.get_inactive_members import get_inactive_members
from server_helper_scripts.get_last_tag_event import get_last_tag_event
from server_helper_scripts.sync_from_fortnox import sync_from_fortnox
from statistics_scripts.generate_statistics import GenerateStats

User = user.User
Sqluser = sql_user.SQLUser
Sql_detailed_tag = sql_tagevent.SQLDetailedTagevent
Tagevent = tagevent.Tagevent
Debt = debt.Debt
DetailedTagevent = detailedtagevent.DetailedTagevent

app.config.from_pyfile('config.py')
app_name = 'crosstag'
version = 'v1.0'
last_tag_events = None


def redirect_not_logged_in():
    flash('You need to login before entering the application')
    return redirect('/')


def check_session():
    if session.get('loggedIn') is not None:
        if session['loggedIn'] and session.get('username') is not None:
            return True
        else:
            return False
    return False


@app.route('/')
@app.route('/index')
def index():
    if check_session():
        return render_template('index.html')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if not check_session():
            form = Login()
            if form.validate_on_submit():
                cl = registration_client.RegisterLoginSqlClient()
                stored_hash = cl.do_login(form.username.data)
                if stored_hash is not None:
                    if bcrypt.hashpw(form.password.data, stored_hash) == stored_hash:
                        # Use above to match passwords
                        session['loggedIn'] = True
                        session['username'] = form.username.data
                        flash('Welcome %s' % form.username.data)
                        return redirect('/')
                    else:
                        flash('Wrong username or password')
                else:
                    flash('Wrong username')

            return render_template('login.html', title='Login', form=form)
        else:
            return redirect('/')
    except:
        flash('Error Trying to login, please try again.')
        return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('loggedIn', None)
    session.pop('username', None)
    return redirect('/')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        if not check_session():
            form = Register()
            if form.validate_on_submit():
                # 1 Get password from form
                password = form.password.data.encode('utf-8')
                # 2 Hash the password
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                # 3 Save the Tenant in the db
                registered_tenant = {'username': form.username.data,
                                     'password': hashed_password,
                                     'active_fortnox': form.active_fortnox.data,
                                     'gym_name': form.gym_name.data,
                                     'address': form.address.data,
                                     'phone': form.phone.data,
                                     'zip_code': form.zip_code.data,
                                     'city': form.city.data,
                                     'email': form.email.data,
                                     'pass': registration_client.cfg.TENANT_PASSWORD + form.username.data}

                cl = registration_client.RegisterLoginSqlClient()
                if cl.do_registration(registered_tenant):
                    flash('Registration done, you can now log in')
                    return redirect('/')

            return render_template('register.html', title='Register new Tenant', form=form)
        else:
            return redirect('/')

    except:
        flash('Error when trying to register, please try again.')
        return redirect('/')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    try:
        if check_session():

            clt = update_tenant_client.UpdateTenantInformationSqlClient()
            current_tenant = clt.get_tenants(session['username'])[0]

            if current_tenant is None:
                return "No user have this ID"

            form = EditTenant(obj=current_tenant)

            if form.validate_on_submit():
                # Get Tenants password for confirmation
                cl = registration_client.RegisterLoginSqlClient()
                stored_hash = cl.do_login(session['username'])

                if stored_hash is not None:
                    hashed_pass = bcrypt.hashpw(form.password.data, stored_hash)

                    # Saves new pass from form
                    hashed_new_pass = form.new_password.data
                    # if the new pass is not empty, hash it
                    if hashed_new_pass is not '':
                        hashed_new_pass = bcrypt.hashpw(hashed_new_pass, bcrypt.gensalt())

                    tenant = {'id': current_tenant.id,
                              'password': hashed_pass,
                              'new_password': hashed_new_pass,
                              'active_fortnox': form.active_fortnox.data,
                              'image': form.image.data,
                              'background_color': form.background_color.data}
                    clt.update_tenant_information(tenant)

                    return redirect('/')

            return render_template('settings.html', title='Settings Tab',
                                   form=form,
                                   data=current_tenant.dict(),
                                   error=form.errors)
        else:
            return redirect('/')
    except:
        flash('Error Updating information, please try again.')
        return redirect('/')

@app.route('/general_information', methods=['GET', 'POST'])
def general_information():
    try:
        if check_session():
            clt = update_tenant_client.UpdateTenantInformationSqlClient()
            current_tenant = clt.get_tenants(session['username'])[0]

            if current_tenant is None:
                return "No user have this ID"

            form = EditGeneralInformation(obj=current_tenant)

            if form.validate_on_submit():
                # Get Tenants password for confirmation
                cl = registration_client.RegisterLoginSqlClient()
                stored_hash = cl.do_login(session['username'])

                if stored_hash is not None:
                    hashed_pass = bcrypt.hashpw(form.password.data, stored_hash)

                    tenant = {'id': current_tenant.id,
                              'password': hashed_pass,
                              'gym_name': form.gym_name.data,
                              'address': form.address.data,
                              'phone': form.phone.data,
                              'zip_code': form.zip_code.data,
                              'city': form.city.data,
                              'email': form.email.data}
                    clt.update_tenant_general_information(tenant)

                    return redirect('/')

            return render_template('general_information.html', title='General Information Tab',
                                   form=form,
                                   data=current_tenant.dict(),
                                   error=form.errors)
        else:
            return redirect('/')
    except:
        flash('Error Updating general information, please try again.')
        return redirect('/')


@app.route('/fortnox_information', methods=['GET', 'POST'])
def fortnox_information():
    try:
        if check_session():
            form = EditFortnoxInformation()
            return render_template('fortnox_information.html', title='Settings Tab',
                                   form=form,
                                   data='',
                                   error=form.errors)
        else:
            return redirect('/')
    except:
        flash('Error Updating fortnox information, please try again.')
        return redirect('/')


# TODO - APIKEY HERE?!
# This function will be called by the javascript on the static_tagin_page
# The function will look for the last tag event and if there is a new tag event,
# it will get the user with the tag and the users all tagevents and send it to the page.
@app.route('/stream')
def stream():
    def up_stream():
        while True:
            global last_tag_events
            tag = get_last_tag_event()
            user = None
            if last_tag_events is None or last_tag_events != tag.index:
                last_tag_events = tag.index

                try:
                    user = User.query.filter_by(tag_id=tag.tag_id).filter(User.status != "Inactive").first().dict()
                except:
                    user = None

                if user is not None:
                    date_handler = lambda user: (
                    user.isoformat()
                    if isinstance(user, datetime)
                    or isinstance(user, date)
                    else None
                    )
                    return 'data: %s\n\n' % json.dumps(user, default=date_handler)

                if user is not None:
                    date_handler = lambda user: (
                    user.isoformat()
                    if isinstance(user, datetime)
                    or isinstance(user, date)
                    else None
                    )
                    return 'data: %s\n\n' % json.dumps(user, default=date_handler)

            return 'data: %s\n\n' % user

    return Response(up_stream(), mimetype='text/event-stream')


# TODO - APIKEY HERE?!
# Renders a static page for the tagin view. Shows the person who tags in.
@app.route('/%s/%s/static_tagin_page' % (app_name, version))
def static_tagin_page():
    return render_template('static_tagin.html',
                           title='Static tagins')


# TODO - APIKEY HERE?!
# Is called by the static page, it will send back an array with the top 5 of..
# those who exercise the most. if there is not five people it will return an empty array.
@app.route('/%s/%s/static_top_five' % (app_name, version))
def static_top_five():
    try:
        users = User.query.filter(User.status != 'Inactive').filter(User.tag_id is not None).filter(User.tag_id != '')\
            .order_by(User.tagcounter.desc()).limit(5)
        arr = []
        if users is not None:
            for user in users:
                person_obj = {'name': user.name, 'amount': user.tagcounter}
                arr.append(person_obj)

        return jsonify({'json_arr': [arr[0], arr[1], arr[2], arr[3], arr[4]]})
    except:
        return jsonify({'json_arr': None})


# TODO - APIKEY HERE?!
# Gets all tags last month, just one event per day.
@app.route('/%s/%s/get_events_from_user_by_tag_id/<tag_id>' % (app_name, version), methods=['GET'])
def get_events_from_user_by_tag_id(tag_id):
    try:
        gs = GenerateStats()
        current_year = gs.get_current_year_string()
        counter = 0
        now = datetime.now()

        users_tagins = Tagevent.query.filter(Tagevent.tag_id.contains(tag_id)).\
            filter(Tagevent.timestamp.contains(current_year)).filter(Tagevent.uid != '').filter(Tagevent.uid is not None)

        for tag_event in users_tagins:
            for days in range(1, 32):
                if tag_event.timestamp.month == now.month:
                    if tag_event.timestamp.day == days:
                        counter += 1
                        break

        return {"value": counter}
    except:
        return {"value": 0}


# TODO - APIKEY HERE?!
# Retrieves a tag and stores it in the database.
@app.route('/%s/%s/tagevent/<tag_id>/<api_key>' % (app_name, version))
def tagevent(tag_id, api_key):
    try:
        cl = registration_client.RegisterLoginSqlClient()
        username = cl.get_tenant_with_api_key(api_key)

        # Test api key: 2F80D9B8-AAB1-40A1-BC26-5DA4DB3E9D9B
        cl = user_client.UsersSqlClient(username[0]['username'])
        user = cl.search_user_on_tag(tag_id)

        tmp__detailed_tagevent = Sql_detailed_tag(None, tag_id, None, user[0][0])

        cl = tag_client.TageventsSqlClient(username[0]['username'])
        cl.add_tagevents(tmp__detailed_tagevent.dict())

        return "%s server tagged %s" % (datetime.now(), tag_id)
    except:
        return "Can't create a tag with that Tag ID or Api Key"


# Returns the last tag event
@app.route('/%s/%s/last_tagin' % (app_name, version), methods=['GET'])
def last_tagin():
    try:
        return Tagevent.query.all()[-1].json()
    except:
        return jsonify({})


# Renders a HTML page with filter on membership
@app.route('/all_users/<filter>', methods=['GET', 'POST'])
def all_users(filter=None):
    try:
        if check_session():
            ret, users = [], []

            cl = user_client.UsersSqlClient()
            users = cl.get_users(0)

            # List users depending on the membership
            if filter != 'all':
                users = [x for x in users if x.status == filter.title()]

            users = sorted(users, key=lambda user: user.firstname)
            for hit in users:
                js = hit.dict()
                ret.append(js)
            return render_template('all_users.html',
                                   title='All Users',
                                   hits=ret,
                                   filter=filter,
                                   count=len(users))
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Showing all users, please try again.')
        return redirect('/')


# Returns a user based on tag_id, in form of a dictionary
@app.route('/%s/%s/get_user_data_tag_dict/<tag_id>' % (app_name, version), methods=['GET'])
def get_user_data_tag_dict(tag_id):
    if check_session():
        user = User.query.filter_by(tag_id=tag_id).first()
        return user.dict()
    else:
        return redirect_not_logged_in()


# Renders a HTML page with the last 10 tag events
@app.route('/last_tagins', methods=['GET'])
def last_tagins():
    try:
        if check_session():
            ret = []
            cl = tag_client.TageventsSqlClient()
            detailed_tagevents = cl.get_detailed_tagevents(0, 10)

            for hit in detailed_tagevents:
                js = hit.dict()
                ret.append(js)

            return render_template('last_tagevents.html',
                                   title='Last Tagins',
                                   hits=ret)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error showing last tagins, please try again.')
        return redirect('/')


# Deletes an user from the local DB based on their index
@app.route('/%s/%s/remove_user/<user_id>' % (app_name, version), methods=['POST'])
def remove_user(user_id):
    try:
        if check_session():
            cl = user_client.UsersSqlClient()
            cl.remove_user(user_id)
            flash('Member was removed!')
            return redirect("/all_users/all")
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Removing a user, please try again.')
        return redirect('/')

# Adds an user to the local DB. Gets all the values from a form in the HTML page.
@app.route('/new_user', methods=['GET', 'POST'])
def add_new_user():
    try:
        if check_session():
            form = NewUser()
            if form.validate_on_submit():
                mc = user_client.UsersSqlClient()

                tmp_usr = Sqluser(None, None, form.firstname.data, form.lastname.data, form.email.data, form.phone.data,
                               form.address.data, form.address2.data, form.city.data,
                               form.zip_code.data, form.tag_id.data, form.gender.data, form.ssn.data, form.expiry_date.data,
                               None, form.status.data, None, None)
                mc.add_user(tmp_usr.dict())

                flash('Created new user: %s %s' % (form.firstname.data, form .lastname.data))
                # tagevent = get_last_tag_event()
                #fortnox_data = Fortnox()
                #fortnox_data.insert_customer(tmp_usr)
                msg = None
                # if tagevent is None:
                    # msg = None
                # else:
                    # msg = (tmp_usr.index, tagevent.tag_id)
                form = NewUser()
                return render_template('new_user.html',
                                       title='New User',
                                       form=form,
                                       message=msg)
            return render_template('new_user.html',
                                   title='New User',
                                   form=form)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Creating a new user, please try again.')
        return redirect('/')

# TODO - SHALL IT EXIST OR NOT?!
# Renders a HTML page which has the same function as the crosstag_reader dummy function.
@app.route('/tagin_user', methods=['GET', 'POST'])
def tagin_user():
    if check_session():
        form = NewTag(csrf_enabled=False)
        now = datetime.now()
        currenthour = now.hour
        nowtostring = str(now)
        timestampquery = nowtostring[:10]
        print(str(form.validate_on_submit()))
        print("errors", form.errors)
        if form.validate_on_submit():
            tmp_tag = Tagevent.query.filter(Tagevent.timestamp.contains(timestampquery)).filter(Tagevent.clockstamp.contains(currenthour)).first()
            user = User.query.filter(User.tag_id == form.tag_id.data).first()
            detailedtag = DetailedTagevent(form.tag_id.data)
            db.session.add(detailedtag)
            if user is not None:
                user.tagcounter += 1
                user.last_tag_timestamp = now
                if tmp_tag is None or tmp_tag == None:
                    tmp_tag = Tagevent()
                    tmp_tag.amount = 1
                    db.session.add(tmp_tag)
                else:
                    tmp_tag.amount += 1
            db.session.commit()
            flash('New tag created')
            return render_template('tagin_user.html',
                                   title='New tag',
                                   form=form)
        return render_template('tagin_user.html', title='New tag', form=form)
    else:
        return redirect_not_logged_in()


# Renders a HTML page with a form to search for a specific user or many users.
@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    try:
        if check_session():
            form = SearchUser()
            if form.validate_on_submit():
                mc = user_client.UsersSqlClient()

                tmp_usr = Sqluser(None, None, form.firstname.data, form.lastname.data, form.email.data, None, None, None,
                                  form.city.data, None, None, None, None, None, None, None, None, None)

                users = mc.search_user(tmp_usr.dict())

                return render_template('search_user.html',
                                       title='Search User',
                                       form=form,
                                       hits=users)
            return render_template('search_user.html',
                                   title='Search User',
                                   form=form)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Searching for a user, please try again.')
        return redirect('/')


# Will bind the last tag to an user by a POST, when finished it will redirect to the "edit user" page.
@app.route('/%s/%s/link_user_to_last_tag/<user_id>' % (app_name, version), methods=['GET', 'POST'])
def link_user_to_last_tag(user_id):
    try:
        if check_session():
            try:
                tc = tag_client.TageventsSqlClient()
                tagevent = tc.get_detailed_tagevents(0, 1)[0]

                cl = user_client.UsersSqlClient()
                user = cl.get_users(user_id)[0]

                if user is None:
                    return "No user have this ID"

                user.tag_id = tagevent.tag_id
                cl.update_user(user.dict())

                return redirect("/edit_user/"+str(user_id))
            except:
                flash("No tagging has happened")
                return redirect("/edit_user/"+str(user_id))
        else:
            return redirect_not_logged_in()
    except:
        flash('Error linking user to last tag, please try again.')
        return redirect('/')

#TODO - APIKEY OR SESSION?
# Returns an users tag.
@app.route('/%s/%s/get_tag/<user_index>' % (app_name, version), methods=['GET'])
def get_tag(user_index):
    user = User.query.filter_by(index=user_index).first()
    return str(user.tag_id)


# Returns the 20 last tag events by a user.
@app.route('/%s/%s/get_tagevents_user_dict/<user_index>' % (app_name, version), methods=['GET'])
def get_tagevents_user_dict(user_index):
    tc = tag_client.TageventsSqlClient()
    tagevent = tc.get_detailed_tagevents(user_index, 20)

    return tagevent


# Renders a HTML page with all inactive members.
@app.route('/inactive_check', methods=['GET'])
def inactive_check():
    if check_session():
        return render_template('inactive_check.html',
                               title='Check',
                               hits=get_inactive_members())
    else:
        return redirect_not_logged_in()


# Delets a debt from a user. Redirects to "user page"
@app.route('/debt_delete/<debt_id>/<user_id>', methods=['POST'])
def debt_delete(debt_id, user_id):
    try:
        if check_session():
            dcl = debt_client.DebtSqlClient()
            dcl.remove_debt(debt_id)
            flash('Debt was deleted!')
            return redirect("/user_page/"+str(user_id))
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Deleting debt, please try again.')
        return redirect('/')


# Renders a HTML page with all users and their debts
@app.route('/debts', methods=['GET'])
def debt_check():
    try:
        if check_session():
            dcl = debt_client.DebtSqlClient()
            debt_array = dcl.get_debt()

            return render_template('debt_check.html',
                                   title='Check',
                                   hits=debt_array)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Showing debt, please try again.')
        return redirect('/')


# Renders a HTML page with a new created debt
@app.route('/debt_create/<user_id>', methods=['GET', 'POST'])
def debt_create(user_id):
    try:
        if check_session():
            cl = user_client.UsersSqlClient()
            dcl = debt_client.DebtSqlClient()
            user = cl.get_users(user_id)[0]
            form = NewDebt()

            if form.validate_on_submit():
                debt = sql_debt.SQLDebt(form.amount.data, user.id, form.product.data, None, None)
                dcl.add_dept(debt.dict())
                flash('Debt added for %s' % (user.firstname + " " + user.lastname))
                return redirect("/user_page/" + user_id)

            return render_template('debt_create.html',
                                   title='Debt Create',
                                   form=form,
                                   error=form.errors)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Creating debt, please try again.')
        return redirect('/')

# Renders a HTML page with all the statistics
@app.route('/statistics', methods=['GET'])
def statistics():
    if check_session():
        default_date = datetime.now()
        default_date_array = {'year': str(default_date.year), 'month': str(default_date.strftime('%m')), 'day':str(default_date.strftime('%d'))}
        gs = GenerateStats()

        # users = User.query.all()
        # event = Tagevent
        ucl = user_client.UsersSqlClient()
        tcl = tag_client.TageventsSqlClient()
        users = ucl.get_users()
        tagevents = tcl.get_statistic_tagevents()
        week_day_name = default_date.strftime('%A')
        month_name = default_date.strftime('%B')
        custom_date_day = {'weekday': week_day_name + ' ' + str(default_date.day) + '/' + str(default_date.month) + '/' +
                           str(default_date.year)}
        custom_date_month = {'month': month_name + ' ' + str(default_date.year)}
        # Send the data to a method who returns an multi dimensional array with statistics.
        ret = gs.get_data(users, tagevents, default_date_array)
        return render_template('statistics.html',
                               plot_paths='',
                               data=ret,
                               data2=custom_date_day,
                               data3=custom_date_month)
    else:
        return redirect_not_logged_in()


# Renders a HTML page based on month, day and year.
@app.route('/<_month>/<_day>/<_year>', methods=['GET'])
def statistics_by_date(_month, _day, _year):
    if check_session():
        chosen_date_array = {'year': _year, 'month': _month, 'day': _day}
        gs = GenerateStats()
        users = User.query.all()
        event = Tagevent
        default_date = datetime.now()
        selected_date = default_date.replace(day=int(_day), month=int(_month), year=int(_year))
        week_day_name = selected_date.strftime('%A')
        month_name = selected_date.strftime('%B')
        custom_date_day = {'weekday': week_day_name + ' ' + str(selected_date.day) + '/' + str(selected_date.month) + '/' + str(selected_date.year)}
        custom_date_month = {'month': month_name + ' ' + str(selected_date.year)}
        # Send the data to a method who returns an multi dimensional array with statistics.
        ret = gs.get_data(users, event, chosen_date_array)
        return render_template('statistics.html',
                               plot_paths='',
                               data=ret,
                               data2=custom_date_day,
                               data3=custom_date_month)
    else:
        return redirect_not_logged_in()


# Syncs the local database with customers from fortnox
@app.route('/%s/%s/fortnox/' % (app_name, version), methods=['GET'])
def fortnox_users():
    try:
        if check_session():
            sync_from_fortnox()
            return redirect("/")
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Syncing from fortnox, please try again.')
        return redirect('/')


# Returns an array with recent tag events
# TODO - EITHER SESSION OR API KEY
@app.route('/getrecentevents', methods=['GET'])
def get_recent_events():
    three_months_ago = datetime.now() - timedelta(weeks=8)
    tags = Tagevent.query.filter(Tagevent.timestamp > three_months_ago).all()
    tags_json = {}

    for tag in tags:
        current = str(tag.timestamp.date())
        if current in tags_json:
            tags_json[current] += 1
        else:
            tags_json[current] = 1

    # add zeroes to all the unvisited days
    tmp_date = three_months_ago.date()
    while tmp_date < datetime.now().date():
        if str(tmp_date) in tags_json:
            pass
        else:
            tags_json[str(tmp_date)] = 0
        tmp_date = tmp_date + timedelta(days=1)

    res = [{'datestamp': x, 'count': y} for x, y in tags_json.iteritems()]
    return json.dumps(res)


# Renders a HTML page with a user and it debts
@app.route('/user_page/<user_index>', methods=['GET', 'POST'])
def user_page(user_index=None):
    try:
        if check_session():
            debts, tagevents = [], []
            cl = user_client.UsersSqlClient()
            dbl = debt_client.DebtSqlClient()
            user = cl.get_users(user_index)[0]

            if user is None:
                return "No user Found"
            else:
                retdepts = dbl.get_debt(user.id)
                if retdepts is not []:
                    for debt in retdepts:
                        js = debt.dict()
                        debts.append(js)
                tagevents = get_tagevents_user_dict(user_index)
                return render_template('user_page.html',
                                       title='User Page',
                                       data=user.dict(),
                                       tags=tagevents,
                                       debts=debts)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Showing a user page, please try again.')
        return redirect('/')


# TODO - WHAT SHOULD WE DO HERE
@app.route('/%s/%s/clear_tagcounter/' % (app_name, version), methods=['GET'])
def clear_tagcounter():
    users = User.query.filter(User.tagcounter > 0)
    if users is None:
            print("she wrote upon it; no such number, no such zone")
    for user in users:
        user.tagcounter = 0

    db.session.commit()
    return redirect('/')


# Renders a HTML page to edit an user
@app.route('/edit_user/<user_index>', methods=['GET', 'POST'])
def edit_user(user_index=None):
    try:
        if check_session():
            cl = user_client.UsersSqlClient()
            user = cl.get_users(user_index)[0]

            if user is None:
                return "No user have this ID"

            form = EditUser(obj=user)
            tagevents = []
            #tagevents = get_tagevents_user_dict(user_index)
            if form.validate_on_submit():
                user.firstname = form.firstname.data
                user.lastname = form.lastname.data
                user.email = form.email.data
                user.phone = form.phone.data
                user.address = form.address.data
                user.address2 = form.address2.data
                user.city = form.city.data
                user.zip_code = form.zip_code.data
                user.tag_id = form.tag_id.data
                user.gender = form.gender.data
                user.expiry_date = form.expiry_date.data
                user.status = form.status.data

                cl.update_user(user.dict())
                # If we successfully edited the user, redirect back to userpage.
                # fortnox_data = Fortnox()
                # fortnox_data.update_customer(user)
                return redirect("/user_page/"+str(user.id))

            if user:
                return render_template('edit_user.html',
                                       title='Edit User',
                                       form=form,
                                       data=user.dict(),
                                       tags=tagevents,
                                       error=form.errors)
            else:
                return "she wrote upon it; no such number, no such zone"
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Editing a user, please try again.')
        return redirect('/')

# TODO - APIKEY HERE?
@app.route('/%s/%s/link_user_to_tag/<user_index>/<tag_id>' % (app_name, version), methods=['POST'])
def link_user_to_tag(user_index, tag_id):
    user = User.query.filter_by(index=user_index).first()
    user.tag = tag_id
    db.session.commit()
    return "OK"

if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] arg \nTry this: " +
                          "python crosstag_server.py", version="%prog 1.0")
    parser.add_option('--debug', dest='debug', default=False, action='store_true',
                      help="Do you want to run this thing with debug output?")
    (options, args) = parser.parse_args()
    # config['database_file'] = options.database
    # config['secret_key'] = options.secret
    db.create_all()
    # if options.debug:
    app.logger.propagate = False
    app.run(host='0.0.0.0', port=app.config["PORT"], debug=True)
