import time
import pandas as pd
import numpy as np
import datetime as dt # prefer to use this module than time as it has more functionalities for dates
import calendar # gain access to calendar dictionaries

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


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
    city_input = input("Would you like to explore Chicago, New York City, Washington or all?").lower()    
    #### will catch if the entry is not part of the current datasets
    while (city_input not in CITY_DATA) and (city_input != 'all'):
        city_input = input("I'm sorry we can't explore that city right now or the city is mispelled. Would you like to explore Chicago, New York City or Washington?").lower()

    # get user input for month (all, january, february, ... , june)
    month_input = input("What month are we looking at? Please enter the entire name or 'all\'.").title()   
    #### will catch if the entry mispelled
    while (month_input not in calendar.month_name) and (month_input != 'All'):
       month_input = input("I think the month is mispelled. Please re-enter the month.").title()
       
    # get user input for day of week (all, monday, tuesday, ... sunday)
    dow_input = input("Day of the week should we focus on? Please enter the entire name or enter 'all\'.").title()   
    #### will catch if the entry mispelled
    while (dow_input not in calendar.day_name) and (dow_input != 'All'):
       dow_input = input("I think the week day is mispelled. Please re-enter the day of the week or enter 'all\'.").title()

    print('-'*40)
    return city_input, month_input, dow_input


def load_data(city_input, month_input, dow_input):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city>>city_input - name of the city to analyze
        (str) month>>month_input - name of the month to filter by, or "all" to apply no month filter
        (str) day>>dow_input - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """         
    # load data file into a dataframe
    df = pd.read_csv(f"./{CITY_DATA[city_input]}")

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month_input != 'All':
        # use month list built into calendar module
        month = list(calendar.month_name).index(month_input)
        if month in df['month'].values:
            # filter by month to create the new dataframe
            df = df[df['month'] == month]
        else:
            print("Sorry, this month is not in the dataset for this city. Let's restart so you can choose a new city and/or month\n")
            get_filters()

    # filter by day of week if applicable
    if dow_input != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == dow_input]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_mode = df['month'].mode()[0]
    print(f"The most common month to travel is in {calendar.month_name[month_mode]}" )

    # display the most common day of week
    dow_mode = df['day_of_week'].mode()[0]
    print(f"The most common day of the week to travel is on {dow_mode}" )

    # display the most common start hour
    start_hr_mode = df['Start Time'].dt.hour.mode()[0]
    if start_hr_mode == 12:
        start_hr_mode_12 = str(start_hr_mode) + " PM" # accommodates for noon
    elif start_hr_mode > 12: 
        start_hr_mode_12 = str(start_hr_mode - 12) + " PM" # accommodates for evening hours, so military time isn't given
    else: 
        start_hr_mode_12 = str(start_hr_mode) + " AM"
# *** TO DO: Change hour to AM/PM format  
    print(f"The most common hour of the day to start a rental is {start_hr_mode_12}" )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_mode = df['Start Station'].mode()[0]
    print(f"The most common station to pick up a bike is at {start_station_mode} station")

    # display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    print(f"The most common station to drop off a bike is {end_station_mode} station")

   # test = df[['Start Station', 'End Station']]
   # print(test.value_counts(['Start Station', 'End Station']))
    # display most frequent combination of start station and end station trip

    df['Start to End Stations'] = df['Start Station'] + ' to ' + df['End Station']
    trip_stations_mode = df['Start to End Stations'].mode()[0] 
    print(f"The most common trips are from {trip_stations_mode} stations")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration_sum_min = df['Trip Duration'].sum()
    duration_sum_hr_part, duration_sum_min_part = divmod(duration_sum_min, 60)
    print(f"The total amount of time all bikes have been used is for {duration_sum_hr_part} hours and {duration_sum_min_part} minutes.")

    # display mean travel time
    duration_mean = df['Trip Duration'].mean()
    duration_mean_hr_part, duration_mean_min_part = divmod(duration_mean, 60)
    print(f"The average trip time is for {int(duration_mean_hr_part)} hours and {int(duration_mean_min_part)} minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    all_users_count = len(df.index)

    print("The number of bikeshare user types:")
    for index, count in enumerate(user_type_count):
        print(f"   {user_type_count.index[index]} : {count}  ({int((count/all_users_count)*100)}%)")

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print("\nThe number of users by gender:")
        for index, count in df.itertuples(gender_count):
            print(f"   {gender_count.index[index]} : {count} ({int((count/all_users_count)*100)}%)")
    except: print('\nGender is unavailable for this city')

    # Display earliest, most recent, and most common year of birth
    try:
        dob_min = df['Birth Year'].min()
        dob_max = df['Birth Year'].max()
        dob_mode = df['Birth Year'].mode()[0]
        print(f"\nCommon user birth year stats:\n   The eldest user was born in {int(dob_min)}\n   The youngest user was born in {int(dob_max)}\n   Most users were born in {int(dob_mode)}")
    except: print('\nBirth data is unavailable for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def see_data(df):
    """Displays rows of raw data upon request."""

    start = 0
    end = 5
    print(df.iloc[start:end])

    more_data_input = input("Would you like to see more raw data?").lower()

    while more_data_input == 'yes' or more_data_input == 'y':
        start += 5
        end += 5
        print(df.iloc[start:end])
        more_data_input = input("Would you like to see more raw data?").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        rawdata_input = input("Would you like to see a sample of raw data?").lower()    
        #### will catch if the entry is not yes or no
        while (rawdata_input != 'yes') and (rawdata_input != 'no') and (rawdata_input != 'y') and (rawdata_input != 'n'):
            rawdata_input = input("I'm sorry, your response was not understood. Please enter yes or no").lower()

        if rawdata_input == 'yes' or rawdata_input == 'y':
            see_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()