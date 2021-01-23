import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def display_raw_data(df):
    """ prompt the user if they want to see 5 lines of raw data,
     display that data if the answer is 'yes',
     and continue these prompts and displays until the user says 'no'. """
    i = 0
    while True:
        raw = input("Would you like to view 5 rows of raw data?, Please enter 'yes' or 'no'\n")
        if raw.lower() in ['yes','no']:
            break
    # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:
        if raw.lower() == 'no':
            break
        print(df[i:i+5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
        while True:
            raw = input("Would you like to view 5 more rows?, Please enter 'yes' or 'no'\n") # TO DO: convert the user input to lower case using lower() function
            if raw.lower() in ['yes','no']:
                break
        i += 5

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
    cities= ["Washington","New York City", "Chicago"]
    while True:
        city = input("Please enter the name of the city you would like to explore.\n Choose from New York City, Chicago, Washington.\n")
        if city.title() in cities:
            break
        print("Please enter a name of a valid city.\n")
    # get user input for month (all, january, february, ... , june)
    months= ["January","February","March","April","May","June"]
    while True:
        m = input("Please enter which month you would like to explore.\nChoose a month from January to June or type 'ALL' to explore all months.\n")
        if m.title() in months:
            month=m
            break
        elif m.upper() == "ALL":
            m = months
            month="all"
            break
        print("Please enter which month you would like to explore.\nType a month from January to June or 'ALL' to explore all months.\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days= ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    while True:
        d = input("Please enter which day you would like to explore.\nChoose a day from Monday to Sunday or type 'ALL' to explore all days.\n")
        if d.title() in days:
            day=d
            break
        elif d.upper() == "ALL":
            d = days
            day="all"
            break
        print("Please enter which day you would like to explore.\nType a day from Monday to Sunday or 'ALL' to explore all days.\n")

    city = city.title()
    month = month.lower()
    day = day.lower()
    print("You have selected {} city to explore, during {} month(s) and on {} day(s)".format(city,month,day))
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
    print("fetching the data from file: {}".format(CITY_DATA[city]))
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df,day,month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month.lower() == 'all':
        popular_month = df['month'].mode()[0]
        print('Most Common Month:', popular_month)

    # display the most common day of week
    if day.lower() == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('Most Common Day Of Week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % str(round((time.time() - start_time),4)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most Common Start Station:', popular_start)


    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most Common End Station:', popular_end)


    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station']+ " - " + df['End Station']
    popular_route = df['Route'].mode()[0]
    print('Most Common Route:', popular_route)


    print("\nThis took %s seconds." % str(round((time.time() - start_time),4)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = str(round(total_travel_time, 1))
    print('Total Travel Time (in Seconds) = ', total_travel_time)


    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    avg_travel_time = str(round(avg_travel_time, 1))
    print('Average Travel Time (in Seconds) = ', avg_travel_time)


    print("\nThis took %s seconds." % str(round((time.time() - start_time),4)))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)



    if city.title() in ['Chicago','New York City']:
        # Display counts of gender
        user_genders = df['Gender'].value_counts()
        print(user_genders)
    # Display earliest, most recent, and most common year of birth
        common_birth = int(df['Birth Year'].mode()[0])
        print("Most common birth year: ",common_birth)
        recent_year = int(df['Birth Year'].max())
        print("Most recent birth year: ",recent_year)
        earliest_year = int(df['Birth Year'].min())
        print("Earlist birth year: ",earliest_year)


    print("\nThis took %s seconds." % str(round((time.time() - start_time),4)))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,day,month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)

        while True:
            restart = input("\nWould you like to restart?\nPlease enter 'yes' to restart, or 'no' if you would like to quit.\n")
            if restart.lower() in ['yes','no']:
                break
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
