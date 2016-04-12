from server_helper_scripts.strip_ssn import strip_ssn
from server_helper_scripts.get_gender_from_ssn import get_gender_from_ssn
from crosstag_init import db
from db_models.user import User


def add_user_to_local_db_from_fortnox(customer):
    """
    Helper script to add a customer from fortnox to the local database.

    :param customer: Takes a customer object as argument
    :type customer: JSON
    """
    tmp_usr = User(customer['Name'], customer['Email'], customer['Phone'],
                   customer['Address1'], customer['Address2'], customer['City'],
                   customer['Zipcode'], None, customer['FortnoxID'],
                   None, strip_ssn(customer),
                   get_gender_from_ssn(customer), None)
    tmp_usr.status = 'Inactive'
    db.session.add(tmp_usr)
    db.session.commit()
