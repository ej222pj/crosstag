# -*- coding: utf-8 -*-
import json
import smtplib
import bcrypt
from datetime import datetime, timedelta
from optparse import OptionParser
import config as cfg
from crosstag_init import app, jsonify, render_template, flash, redirect, Response, session
from db_service import register_login_sql_client as registration_client
from db_service import users_sql_client as user_client
from db_service import debt_sql_client as debt_client
from db_service import update_tenant_information_sql_client as update_tenant_client
from db_service import tagevents_sql_client as tag_client
from db_models import sql_user
from db_models import sql_debt
from db_models import sql_detailed_tagevent
from forms.edit_user import EditUser
from forms.new_debt import NewDebt
from forms.new_user import NewUser
from forms.search_user import SearchUser
from forms.login import Login
from forms.registration import Register
from forms.edit_tenant import EditTenant
from forms.edit_general_information import EditGeneralInformation
from forms.edit_fortnox_information import EditFortnoxInformation
from fortnox.fortnox import Fortnox
from server_helper_scripts.sync_from_fortnox import sync_from_fortnox
from statistics_scripts.generate_statistics import GenerateStats

Sqluser = sql_user.SQLUser
Sql_detailed_tag = sql_detailed_tagevent.SQLDetailedTagevent

app.config.from_pyfile('config.py')
app_name = 'crosstag'
version = 'v2.0'


def redirect_not_logged_in():
    """
    Redirect the page if the tenant is not logged in and is trying to reach a page without permission

    :return: redirect to front page
    """
    flash('You need to login before entering the application')
    return redirect('/')


def check_session():
    """
    Checks if the tenant is logged in by checking the session for username param and loggedin param
    This function is called by all other functions that handle tenant templates

    :return: True or false
    """
    if session.get('loggedIn') is not None:
        if session['loggedIn'] and session.get('username') is not None:
            return True
        else:
            return False
    return False


@app.route('/')
@app.route('/index')
def index():
    """
    Render index template if the user is logged in, if not the user is redirected to the login page

    :return: render template or redirect
    """
    if check_session():
        return render_template('index.html')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET - Renders a login template for the tenant
    POST - Validates the login form and check if the values are right. If they pass the tenant is logged in and redirected
    to the front page again, if not the login templated is rendered with an message.

    :return: Redirect or renders template
    """
    try:
        if not check_session():
            form = Login()
            if form.validate_on_submit():
                cl = registration_client.RegisterLoginSqlClient()
                stored_hash = cl.do_login(form.username.data.title())
                if stored_hash is not None:
                    if bcrypt.hashpw(form.password.data, stored_hash) == stored_hash:
                        # Use above to match passwords
                        session['loggedIn'] = True
                        session['username'] = form.username.data.title()
                        flash('Welcome %s' % form.username.data.title())
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
    """
    Logouts the tenant. Destroys the session and redirects to the front page again.

    :return: redirect
    """
    session.pop('loggedIn', None)
    session.pop('username', None)
    return redirect('/')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    """
    GET - Renders a registration form.
    POST - Validates the login form and check if the values are right. If they pass the informations is stored in
    the database and the tenant is registrated and is redirected to the front page.
    If they fail the registration form is rendered with error messages.

    :return: Redirect or renders template
    """
    try:
        if not check_session():
            form = Register()
            if form.validate_on_submit():
                # TODO: Remove temporally disabled registration, 2 lines below
                flash('Registration is temporarily disabled.')
                return redirect('/')
                '''
                # 1 Get password from form
                password = form.password.data.encode('utf-8')
                # 2 Hash the password
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                # 3 Save the Tenant in the db
                registered_tenant = {'username': form.username.data.title(),
                                     'password': hashed_password,
                                     'active_fortnox': form.active_fortnox.data,
                                     'gym_name': form.gym_name.data,
                                     'address': form.address.data,
                                     'phone': form.phone.data,
                                     'zip_code': form.zip_code.data,
                                     'city': form.city.data,
                                     'email': form.email.data,
                                     'pass': registration_client.cfg.TENANT_PASSWORD + form.username.data.title()}

                cl = registration_client.RegisterLoginSqlClient()
                if cl.do_registration(registered_tenant):
                    flash('Registration done, you can now log in')
                    return redirect('/')
                else:
                    flash('Username already exists')
                '''

            return render_template('register.html', title='Register new Tenant', form=form, errors=form.errors)
        else:
            return redirect('/')
    except:
        flash('Error when trying to register, please try again.')
        return redirect('/')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """
    GET - Renders a settings form with tenant information
    POST - Validates the settings form and check if the values are right. If they pass the informations is stored in
    the database and the tenant is redirected to the front page.
    If they fail the settings form is rendered with error messages.

    :return: Redirect or renders template
    """
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
                    if hashed_pass == stored_hash:
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
                        flash('Gym information changed')
                        return redirect('/')
                    else:
                        flash('Wrong password, could not save changes')

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
    """
    GET - Renders a settings form with general information.
    POST - Validates the settings form and check if the values are right. If they pass the informations is stored in
    the database and the tenant is redirected to the front page.
    If they fail the settings form is rendered with error messages.

    :return: Redirect or renders template
    """
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
                    if hashed_pass == stored_hash:
                        tenant = {'id': current_tenant.id,
                                  'password': hashed_pass,
                                  'gym_name': form.gym_name.data,
                                  'address': form.address.data,
                                  'phone': form.phone.data,
                                  'zip_code': form.zip_code.data,
                                  'city': form.city.data,
                                  'email': form.email.data}
                        clt.update_tenant_general_information(tenant)
                        flash('Gym information changed')
                        return redirect('/')
                    else:
                        flash('Wrong password, could not save changes')

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
    """
    GET - Renders a settings form for fortnox information
    POST - Validates the settings form and check if the values are right. If they pass the informations is stored in
    the database and the tenant is redirected to the front page.
    If they fail the settings form is rendered with error messages.

    :return: Redirect or renders template
    """
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


# Retrieves a tag and stores it in the database.
@app.route('/%s/%s/tagevent/<tag_id>/<api_key>/<timestamp>' % (app_name, version))
def tagevent(tag_id, api_key, timestamp):
    """
    Gets a tagevent from crosstag_reader with tag_id, api_key and timestamp of the tagevent.
    Checks if the api-key is valid and then creates the tag and saves it in the database.
    If the api-key is wrong a KeyError is raised.

    :param tag_id:
    :param api_key:
    :param timestamp:
    :type tag_id: string
    :type api_key: string
    :type timestamp: string
    :return: Redirect or renders template
    :raises: KeyError
    """
    cl = registration_client.RegisterLoginSqlClient()
    username = cl.get_tenant_with_api_key(api_key)
    if username[0]['username'] is not None:
        try:
            cl = user_client.UsersSqlClient(username[0]['username'])
            user = cl.search_user_on_tag(tag_id)[0][0]
            if user is None:
                id = 0
            else:
                id = user
            timestamp = timestamp.replace('%', ' ')
            tmp__detailed_tagevent = Sql_detailed_tag(None, tag_id, timestamp, id)

            cl = tag_client.TageventsSqlClient(username[0]['username'])
            cl.add_tagevents(tmp__detailed_tagevent.dict())

            return "%s server tagged %s" % (datetime.now(), tag_id)
        except:
                return "Can't create a tag with that Tag ID or Api Key"
    else:
        raise KeyError('Wrong API-Key')


# Renders a HTML page with filter on membership
@app.route('/all_users/<filter>', methods=['GET', 'POST'])
def all_users(filter=None):
    """
    Lists all members based on the filter.

    :param filter:
    :type filter: string
    :return: Redirect or renders template
    """
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


# Renders a HTML page with the last 10 tag events
@app.route('/last_tagins', methods=['GET'])
def last_tagins():
    """
    Lists the last tagins. At the moment ( 2016-05-19 ) it is the last 10 tags, but this will be changeable

    :return: Redirect or renders template
    """
    try:
        if check_session():
            ret = []
            cl = tag_client.TageventsSqlClient()
            detailed_tagevents = cl.get_detailed_tagevents(0, 10)
            return render_template('last_tagevents.html',
                                   title='Last Tagins',
                                   hits=detailed_tagevents)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error showing last tagins, please try again.')
        return redirect('/')


# Deletes an user from the local DB based on their index
@app.route('/%s/%s/remove_user/<user_id>' % (app_name, version), methods=['POST'])
def remove_user(user_id):
    """
    Deletes a user from the database.

    :param user_id:
    :type user_id: integer
    :return: Redirect
    """
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
    """
    GET - Renders a new user form.
    POST - Validates the user form and check if the values are right. If they pass the informations is stored in
    the database and the user is registrated. The tenant is redirected to the user page.
    If they fail the user form is rendered with error messages.

    :return: Redirect or renders template
    """
    try:
        if check_session():
            form = NewUser()
            if form.validate_on_submit():
                mc = user_client.UsersSqlClient()

                tmp_usr = Sqluser(None, None, form.firstname.data, form.lastname.data, form.email.data, form.phone.data,
                               form.address.data, form.address2.data, form.city.data,
                               form.zip_code.data, None, form.gender.data, form.ssn.data, form.expiry_date.data,
                               None, form.status.data, None, None)
                user_id = mc.add_user(tmp_usr.dict())
                return redirect('/user_page/' + str(user_id))

            return render_template('new_user.html',
                                   title='New User',
                                   form=form,
                                   error=form.errors)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Creating a new user, please try again.')
        return redirect('/')


# Renders a HTML page with a form to search for a specific user or many users.
@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    """
    GET - Renders a search user form.
    POST - Takes the value from the form and pass it to the database. Retrieves a list of user/users based on
    the information that was passed.

    :return: Renders template with the search result
    """
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
    """
    Links the user to the last tag. Grabs the last tag stored in the database and binds it to the specified member.
    Grabs only a tag that doesnt belong to another member.

    :param user_id:
    :type user_id: integer
    :return: Redirect to edit user page
    """
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


# Renders a HTML page with all inactive members.
@app.route('/inactive_check', methods=['GET'])
def inactive_check():
    """
    Renders a template with a list of all users that have not tagged in for the last 2 weeks

    :return: Renders template with a user list
    """
    try:
        if check_session():
            ret = []
            mc = user_client.UsersSqlClient()
            users = mc.get_inactive_users()


            return render_template('inactive_check.html',
                                   title='Inactive Members',
                                   hits=users)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Showing Inactive Users, please try again.')
        return redirect('/')

# Delets a debt from a user. Redirects to "user page"
@app.route('/debt_delete/<debt_id>/<user_id>', methods=['POST'])
def debt_delete(debt_id, user_id):
    """
    Deletes a debt from a user and redirect back to the userpage

    :param debt_id:
    :param user_id:
    :type debt_id: integer
    :type user_id: integer
    :return: Redirect to user page
    """
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
    """
    Renders a template with a list of all users with debts

    :return: Renders template with a list of users
    """
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
    """
    GET - Renders a debt form.
    POST - Validates the debt form and check if the values are right. If they pass the informations is stored in
    the database and the debt is registrated. The tenant is redirected to the user page.
    If they fail the debt form is rendered with error messages.

    :param user_id:
    :type user_id: integer
    :return: Redirect to edit user page
    """
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
    """
    Renders statistic from the database on todays date.
    1. Tags by hour
    2. Tags by day
    3. Tags by month
    4. Number of genders in database
    5. Number of tags by gender
    6. Number of age groups in database

    :return: Render template for statistic
    """
    try:
        if check_session():
            default_date = datetime.now()
            default_date_array = {'year': str(default_date.year),
                                  'month': str(default_date.strftime('%m')),
                                  'day':str(default_date.strftime('%d'))}
            gs = GenerateStats()

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
    except:
        flash('Error showing statistic, please try again.')
        return redirect('/')


# Renders a HTML page based on month, day and year.
@app.route('/<_month>/<_day>/<_year>', methods=['GET'])
def statistics_by_date(_month, _day, _year):
    """
    Renders statistic from the database on the specified date from the params.
    1. Tags by hour
    2. Tags by day
    3. Tags by month
    4. Number of genders in database
    5. Number of tags by gender
    6. Number of age groups in database

    :param _month:
    :param _day:
    :param _year:
    :type _month: string
    :type _day: string
    :type _year: string
    :return: Render template for statistic
    """
    try:
        if check_session():
            chosen_date_array = {'year': _year, 'month': _month, 'day': _day}
            gs = GenerateStats()

            ucl = user_client.UsersSqlClient()
            tcl = tag_client.TageventsSqlClient()
            users = ucl.get_users()
            tagevents = tcl.get_statistic_tagevents()

            default_date = datetime.now()
            selected_date = default_date.replace(day=int(_day), month=int(_month), year=int(_year))
            week_day_name = selected_date.strftime('%A')
            month_name = selected_date.strftime('%B')
            custom_date_day = {'weekday': week_day_name + ' ' + str(selected_date.day)
                                          + '/' + str(selected_date.month)
                                          + '/' + str(selected_date.year)}

            custom_date_month = {'month': month_name + ' ' + str(selected_date.year)}
            # Send the data to a method who returns an multi dimensional array with statistics.
            ret = gs.get_data(users, tagevents, chosen_date_array)
            return render_template('statistics.html',
                                   plot_paths='',
                                   data=ret,
                                   data2=custom_date_day,
                                   data3=custom_date_month)
        else:
            return redirect_not_logged_in()
    except:
        flash('Error showing statistic, please try again.')
        return redirect('/')


# Syncs the local database with customers from fortnox
@app.route('/%s/%s/fortnox/' % (app_name, version), methods=['GET'])
def fortnox_users():
    """
    Syncs the database with users from fortnox database.
    Add or updates the users.

    :return: Redirect to front page
    """
    try:
        if check_session():
            sync_from_fortnox()
            return redirect("/")
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Syncing from fortnox, please try again.')
        return redirect('/')


# Renders a HTML page with a user and it debts
@app.route('/user_page/<user_index>', methods=['GET', 'POST'])
def user_page(user_index=None):
    """
    Renders a template with user information on a specified user.

    :param user_index:
    :type user_index: integer
    :return: Renders a template
    """
    try:
        if check_session():
            debts, tagevents = [], []
            cl = user_client.UsersSqlClient()
            user = cl.get_users(user_index)[0]

            if user is None:
                return "No user Found"
            else:
                dbl = debt_client.DebtSqlClient()
                ret_depts = dbl.get_debt(user.id)
                if ret_depts is not []:
                    for debt in ret_depts:
                        js = debt.dict()
                        debts.append(js)
                tc = tag_client.TageventsSqlClient()
                tagevents = tc.get_detailed_tagevents(user_index, 20)
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


# Renders a HTML page to edit an user
@app.route('/edit_user/<user_index>', methods=['GET', 'POST'])
def edit_user(user_index=None):
    """
    GET - Renders a edit user form.
    POST - Validates the user form and check if the values are right. If they pass the information is stored in
    the database and the user is updated. The tenant is redirected to the user page.
    If they fail the edit user form is rendered with error messages.

    :param user_index:
    :type user_index: integer
    :return: Renders a template
    """
    try:
        if check_session():
            cl = user_client.UsersSqlClient()
            user = cl.get_users(user_index)[0]

            if user is None:
                return "No user have this ID"

            form = EditUser(obj=user)
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
                # Not in use at this point. Will be a future feature..
                # If we successfully edited the user, redirect back to userpage.
                # fortnox_data = Fortnox()
                # fortnox_data.update_customer(user)
                return redirect("/user_page/"+str(user.id))

            if user:
                return render_template('edit_user.html',
                                       title='Edit User',
                                       form=form,
                                       data=user.dict(),
                                       error=form.errors)
            else:
                return "she wrote upon it; no such number, no such zone"
        else:
            return redirect_not_logged_in()
    except:
        flash('Error Editing a user, please try again.')
        return redirect('/')


if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] arg \nTry this: " +
                          "python crosstag_server.py", version="%prog 1.0")
    parser.add_option('--debug', dest='debug', default=False, action='store_true',
                      help="Do you want to run this thing with debug output?")
    (options, args) = parser.parse_args()
    # config['database_file'] = options.database
    # config['secret_key'] = options.secret
    #db.create_all()
    # if options.debug:
    app.logger.propagate = False
    app.run(host='0.0.0.0', port=app.config["PORT"], debug=True)

#
#   THE CODE BELOW IS NOT IN USE. BUT WILL BE USED IN THE NEXT RELEASE OF THE PROGRAM!
#
'''
# TODO - APIKEY HERE?!
# This function will be called by the javascript on the static_tagin_page
# The function will look for the last tag event and if there is a new tag event,
# it will get the user with the tag and the users all tagevents and send it to the page.
@app.route('/stream')
def stream():
    def up_stream():
        while True:
            global last_tag_events
            # tag = get_last_tag_event() - New way exists!!!
            user = None
            if last_tag_events is None or last_tag_events != tag.index:
                last_tag_events = tag.index

                try:
                    user = User.query.filter_by(tag_id=tag.tag_id).filter(
                        User.status != "Inactive").first().dict()
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
#
#   THE CODE BELOW IS NOT IN USE. BUT WILL BE USED IN THE NEXT RELEASE OF THE PROGRAM!
#
# TODO - APIKEY HERE?!
# Renders a static page for the tagin view. Shows the person who tags in.
@app.route('/%s/%s/static_tagin_page' % (app_name, version))
def static_tagin_page():
    return render_template('static_tagin.html',
                           title='Static tagins')
#
#   THE CODE BELOW IS NOT IN USE. BUT WILL BE USED IN THE NEXT RELEASE OF THE PROGRAM!
#
# TODO - APIKEY HERE?!
# Is called by the static page, it will send back an array with the top 5 of..
# those who exercise the most. if there is not five people it will return an empty array.
@app.route('/%s/%s/static_top_five' % (app_name, version))
def static_top_five():
    try:
        users = User.query.filter(User.status != 'Inactive').filter(User.tag_id is not None).filter(
            User.tag_id != '') \
            .order_by(User.tagcounter.desc()).limit(5)
        arr = []
        if users is not None:
            for user in users:
                person_obj = {'name': user.name, 'amount': user.tagcounter}
                arr.append(person_obj)

        return jsonify({'json_arr': [arr[0], arr[1], arr[2], arr[3], arr[4]]})
    except:
        return jsonify({'json_arr': None})

#
#   THE CODE BELOW IS NOT IN USE. BUT WILL BE USED IN THE NEXT RELEASE OF THE PROGRAM!
#
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
'''


