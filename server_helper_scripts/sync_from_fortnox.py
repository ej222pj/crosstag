from crosstag_init import flash
from db_models import sql_user
from fortnox.fortnox import Fortnox
from db_service import users_sql_client as client
from server_helper_scripts.get_gender_from_ssn import get_gender_from_ssn


def sync_from_fortnox():
    """
    Helper script to sync the local database with the content of the database on fortnox.
    Either updates an existing customer or creates a new.
    """
    try:
        fortnox_data = Fortnox()
        customers = fortnox_data.get_all_customers()
        ret = []
        for element in customers:
            for customer in element:
                name = customer['Name'].split()
                if len(name) < 2:
                    name.append('')
                cust = sql_user.SQLUser(None, customer['CustomerNumber'],
                                        name[0], name[1], customer['Email'],
                                        customer['Phone'], customer['Address1'],
                                        customer['Address2'], customer['City'],
                                        customer['ZipCode'], None,
                                        get_gender_from_ssn(customer),
                                        customer['OrganisationNumber'][:-5], None, None, None,
                                        None, None)
                ret.append(cust.dict())

        cl = client.UsersSqlClient()
        for customer in ret:
            if cl.does_user_exist(customer['fortnox_id']):
                cl.add_user(customer)
            else:
                cl.update_user(customer)

        flash("Members from Fortnox is added/updated to the database!")
    except:
        flash("Something happend while adding/updating from fortnox")
