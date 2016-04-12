def strip_ssn(customer):
    """
    Helper script to strip the last 5 characters in the social security number.

    :param customer: Takes a customer as argument
    :type customer: JSON
    :return: Customer object with the new social security number.
    """
    return customer['OrganisationNumber'][:-5]
