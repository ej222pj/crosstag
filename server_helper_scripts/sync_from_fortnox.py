from crosstag_init import flash
from server_helper_scripts.update_user_in_local_db_from_fortnox import update_user_in_local_db_from_fortnox
from server_helper_scripts.add_user_to_local_db_from_fortnox import add_user_to_local_db_from_fortnox
from db_models.user import User
from db_models import sql_user
from fortnox.fortnox import Fortnox
from db_service import members_sql_client as client
from server_helper_scripts.strip_ssn import strip_ssn
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
                cust = sql_user.SQLUser(None, customer['CustomerNumber'],
                                        name[0], name[1], customer['Email'],
                                        customer['Phone'], customer['Address1'],
                                        customer['Address2'], customer['City'],
                                        customer['ZipCode'], None,
                                        get_gender_from_ssn(customer),
                                        strip_ssn(customer), None, None, None,
                                        None, None)
                ret.append(cust.dict())

        cl = client.MembersSqlClient()
        # for customer in ret:
        #     if User.query.filter_by(fortnox_id=customer['FortnoxID']).first() is not None:
        #         update_user_in_local_db_from_fortnox(customer)
        #     else:
        #         add_user_to_local_db_from_fortnox(customer)
        # TODO - Send in customer object instead of all parameters. Do a Stored procedure for updating fortnox user.
        for customer in ret:
            if cl.does_member_exist(customer['fortnox_id']) is None:
                cl.add_member(customer)
            else:
                cl.update_member(customer)

        flash("Members from Fortnox is added to the database!")
    except:
        flash("Error retriving from Fortnox, Wrong credentials?")
