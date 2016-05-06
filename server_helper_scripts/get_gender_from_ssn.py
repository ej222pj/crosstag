def get_gender_from_ssn(customer):
    """
    Helper script to set the gender of a customer from fortnox.

    :param customer: Takes a customer as argument
    :type customer: JSON
    :return: A string of the gender. Female, Male or Unknown
    """
    ssn_gender_number = customer['OrganisationNumber'][-2:]

    try:
        gender_number = int(ssn_gender_number[:1])
        if gender_number % 2 == 0:
            return 'female'
        elif int(gender_number) % 2 == 1:
            return 'male'
        else:
            return 'unknown'
    except:
        return 'unknown'
