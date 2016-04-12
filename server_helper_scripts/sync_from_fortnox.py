from crosstag_init import flash
from server_helper_scripts.update_user_in_local_db_from_fortnox import update_user_in_local_db_from_fortnox
from server_helper_scripts.add_user_to_local_db_from_fortnox import add_user_to_local_db_from_fortnox
from db_models.user import User
from fortnox.fortnox import Fortnox


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

                cust = {'FortnoxID': customer["CustomerNumber"],
                        'OrganisationNumber': customer['OrganisationNumber'],
                        'Name': customer["Name"],
                        'Email': customer['Email'],
                        'Phone': customer['Phone'],
                        'Address1': customer['Address1'],
                        'Address2': customer['Address2'],
                        'City': customer['City'],
                        'Zipcode': customer['ZipCode']}

                ret.append(cust)

        for customer in ret:
            if User.query.filter_by(fortnox_id=customer['FortnoxID']).first() is not None:
                update_user_in_local_db_from_fortnox(customer)
            else:
                add_user_to_local_db_from_fortnox(customer)

        flash("Members from Fortnox is added to the database!")
    except:
        flash("Error retriving from Fortnox, Wrong credentials?")
