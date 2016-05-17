from datetime import datetime, timedelta
from calendar import monthrange


class GenerateStats:
    """
    GenerateStats helps to calculate and generate the data for the statistics.

    get_data - Return an array with every data collected.
    get_all_gender_data - Return an array with the number of all genders by type.
    get_gender_tag_data - Return an array with the amount of tags base on gender.
    get_tagins_by_month - Return an array with the total amount of tagevents from every month
    get_tagins_by_day - Returns an array with the total amount of tagevents per day in a specific month and year
    get_tagins_by_hour - Return and array with the total amount of tagevents per hour on a specific day
    get_age_data - Return an array with amount of customer in different age groups
    get_current_year_string - Returns a string of the current year
    get_current_month_string - Returns a string of the current month
    get_current_day_string - Returns a string of the current day

    """

    def get_data(self, users, tagevent, chosen_date_array):
        """
        Get_data is called from the server to generate data of the database. Returns an multidimensional array with every data
        in different categories.

        :param users: Takes the user database model as argument
        :param tagevent: Takes the tagevent database model as argument
        :param chosen_date_array: Takes a specific date to search from
        :type users: Database model User
        :type tagevent: Database model Tagevent
        :type chosen_date_array: Dictionary
        :return: Multidimensional array with data from every category.
        """
        data = []

        data.append(self.get_all_gender_data(users))
        data.append(self.get_gender_tag_data(users))
        data.append(self.get_tagins_by_month(tagevent, chosen_date_array))
        data.append(self.get_age_data(users))
        # Send year and month
        data.append(self.get_tagins_by_day(tagevent, chosen_date_array))
        # Send year, month and day
        data.append(self.get_tagins_by_hour(tagevent, chosen_date_array))
        return data

    def get_all_gender_data(self, users):
        """
        Calculate the amount of different genders in the database.

        :param users: Takes an array with every user in it
        :type users: Array with user objects
        :return: Array with the amount of different genders in the database.
        """
        male_counter = 0
        female_counter = 0
        unknown_counter = 0

        for hit in users:

            js = hit.gender

            if js == "male":
                male_counter += 1
            if js == "female":
                female_counter += 1
            if js == "unknown":
                unknown_counter += 1

        return [male_counter, female_counter, unknown_counter]

    def get_gender_tag_data(self, users):
        """
        Calculate the amount of tagevents based on gender type.

        :param users: Takes an array with users as argument
        :type users: Array with every user objects.
        :return: Array with the amount of tags based on different genders
        """
        male_counter = 0
        female_counter = 0
        unknown_counter = 0

        for user in users:
            if user.gender == 'male':
                male_counter += user.tagcounter
            elif user.gender == 'female':
                female_counter += user.tagcounter

        return [male_counter, female_counter, unknown_counter]

    def get_tagins_by_month(self, event, chosen_date_array):
        """
        Calculates every tagevent based on year

        :param event: Takes an event database model as argument
        :param chosen_date_array: Takes an array with a specific date as argument
        :type event: Database model
        :type chosen_date_array: Array with dates
        :return: Array with all tagevents from every month
        """
        year_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        timestamps = [x for x in event if chosen_date_array['year'] in x.timestamp]

        for timestamp in timestamps:
            for x in range(1, 13):
                if x < 10:
                    y = chosen_date_array['year'] + '-0' + str(x)
                else:
                    y = chosen_date_array['year'] + '-' + str(x)

                if y == timestamp.timestamp[:7]:
                    year_arr[x-1] += timestamp.amount

        year_arr.append(int(chosen_date_array['year']))
        return year_arr

    def get_tagins_by_day(self, event, chosen_date_array):
        """
        Calculates every tagevent on every day at a specific month and year

        :param event: Takes an event database model as argument
        :param chosen_date_array: Takes an array with a specific date as argument
        :type event: Database model
        :type chosen_date_array: Array with dates
        :return: Array with all tagevents on every day from a specific month and year
        """
        date_query = chosen_date_array['year'] + '-' + chosen_date_array['month']
        useless_tuple = monthrange(int(chosen_date_array['year']), int(chosen_date_array['month']))
        days_in_month = useless_tuple[1]
        day_arr = [0]*days_in_month

        # timestamps = event.query.filter(event.timestamp.contains(date_query))
        timestamps = [x for x in event if date_query in x.timestamp]
        for timestamp in timestamps:
            for x in range(1, days_in_month+1):
                if x < 10:
                    y = date_query + '-0' + str(x)
                else:
                    y = date_query + '-' +str(x)

                if y == timestamp.timestamp[:10]:
                    day_arr[x-1] += timestamp.amount

        return day_arr

    def get_tagins_by_hour(self, event, chosen_date_array):
        """
        Calculates every tagevent on every hour on a specific day

        :param event: Takes an event database model as argument
        :param chosen_date_array: Takes an array with a specific date as argument
        :type event: Database model
        :type chosen_date_array: Array with dates
        :return: Array with all tagevents on every hour from a specific day
        """
        date_query = chosen_date_array['year'] + '-' + chosen_date_array['month'] + '-' + chosen_date_array['day']
        timestamps = event.query.filter(event.timestamp.contains(date_query))

        hour_arr = [0]*24

        for timestamp in timestamps:
            for x in range(1, 25):
                if x == timestamp.clockstamp:
                    hour_arr[x-1] += timestamp.amount

        return hour_arr

    def get_age_data(self, users):
        """
        Calculates the amount of different age groups of all users from the local database.
        1. 15-25
        2. 26-35
        3. 36-45
        4. 46-55
        5. 56-64
        6. 65+

        :param event: Takes an event database model as argument
        :type event: Database model
        :return: Array with the amount of users from all different age groups.
        """

        current_year = int(self.get_current_year_string())
        age_arr = [0, 0, 0, 0, 0, 0]

        for user in users:
            temp_ssn = 0
            if len(user.ssn) == 8:
                temp_ssn = user.ssn[:-4]
                if int(temp_ssn[:-2]) == 19 or int(temp_ssn[:-2]) == 20:
                    age = current_year - int(temp_ssn)
                    if age >= 15 and age <= 25:
                        age_arr[0] += 1
                    if age >= 26 and age <= 35:
                        age_arr[1] += 1
                    if age >= 36 and age <= 45:
                        age_arr[2] += 1
                    if age >= 46 and age <= 55:
                        age_arr[3] += 1
                    if age >= 56 and age <= 64:
                        age_arr[4] += 1
                    if age >= 65:
                        age_arr[5] += 1

        return age_arr

    def get_current_year_string(self):
        """

        :return: Current year as a string
        """
        now = datetime.now()
        current_year = str(now.year)

        return current_year

    def get_current_month_string(self):
        """

        :return: Current month as a string
        """
        now = datetime.now()
        current_month = str(now.month)

        return current_month

    def get_current_day_string(self):
        """

        :return: Current day as a string
        """
        now = datetime.now()
        current_day = str(now.day)

        return current_day
