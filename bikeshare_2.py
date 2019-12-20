import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input("Enter the city (chicago, new york city, washington) you are interested in. \n")
        city = city.lower()
        if city not in cities:
            print("Please enter a valid city name.\n")
        else:
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the month you are intersted in (january, february, ... , june). For all data type \"all\". \n")
        month = month.lower()
        if month not in MONTHS:
            print("Please enter a valid month.\n")
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input("Enter the day of the week you are intersted in (monday, tuesday, ... sunday). For all days type \"all\". \n")
        day = day.lower()
        if day not in days:
            print("Please enter a valid day.\n")
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #Load the data file
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_common = df['month'].value_counts().idxmax()
    print("Most common month is {}.".format(MONTHS[month_common - 1].title()))


    # display the most common day of week
    day_common = df['day_of_week'].value_counts().idxmax()
    print("Most common day of week is {}.".format(day_common.title()))


    # display the most common start hour
    hour_common = df['Start Time'].dt.hour.value_counts().idxmax()
    print("Most common start houd in a day is {}.".format(hour_common))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_count = df['Start Station'].value_counts()
    start_station_common = df['Start Station'].value_counts().idxmax()
    print("Most common start station is {}, and is used {} times.".format(start_station_common, start_station_count[start_station_common]))


    # display most commonly used end station
    end_station_count = df['End Station'].value_counts()
    end_station_common = df['End Station'].value_counts().idxmax()
    print("Most common end station is {}, and is used {} times.".format(end_station_common, end_station_count[end_station_common]))


    # display most frequent combination of start station and end station trip
    start_end_group = df.groupby(['Start Station', 'End Station'])
    start_end_common = start_end_group.count()['Start Time'].idxmax()
    start_end_count = start_end_group.count()['Start Time'].max()
    print("Most common start and end station tiip is {}, and is used {} times.".format(start_end_common, start_end_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_tiem = df['Trip Duration'].sum()
    print("The total travel time is {} seconds.".format(tot_travel_tiem))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is {} seconds.".format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.

    Args:
        (str) city - name of the city to analyze

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The following are the User Type and their counts: \n{}".format(df['User Type'].value_counts()))


    # Display counts of gender
    if city == 'washington':
        print("\nNo Gender and Birth Year data for Washington. Sorry!")
    else:
        print("\nThe following is the Gender distrbution: \n{}".format(df['Gender'].value_counts()))


        # Display earliest, most recent, and most common year of birth
        print("\nThe earliest birth year is {}.".format(int(df['Birth Year'].min())))
        print("The most recent birth year is {}.".format(int(df['Birth Year'].max())))
        print("The most common birth year is {}.".format(int(df['Birth Year'].value_counts().idxmax()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data upon request.

    Args:

    """

    df_size = df.size
    ind = 1
    see_raw_data = input("Would you like to see the raw data? Enter 'y' or 'n'.\n")
    while (ind * 5) < df_size:
        if see_raw_data.lower() == 'y':
            print(df.iloc[((ind - 1) * 5) : (ind * 5)])
        elif see_raw_data.lower() == 'n':
            break
        else:
            print("Choose wisely.\n")
        ind += 1
        see_raw_data = input("Would you like to see the next 5 rows? Enter 'y' or 'n'.\n")

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nIf you like to restart enter \'y\' and press Enter, else just press Enter.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
