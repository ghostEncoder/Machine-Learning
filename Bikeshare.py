import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'C://Users//jedidiah//PycharmProjects//Alpha//Bike_share//chicago.csv',
              'new york city': 'C://Users//jedidiah//PycharmProjects//Alpha//Bike_share//new_york_city.csv',
              'washington': 'C://Users//jedidiah//PycharmProjects//Alpha//Bike_share//washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june','all']
days_list=['monday','tuesday','wednesday','thursday','friday','all']


def get_filters():
    check_data=False
    print('\nHello! Let\'s explore some US bikeshare data!')
    city_1=input("Input Your City Choice! ")
    city_1=city_1.lower()
    month_1=input("Enter Your Filter Month(type 'all' to include all months): ")
    month_1=month_1.lower()
    day_1=input("Enter Your Choice of Week of Day!(type 'all' to include all days): ")
    check_data=check_valid(month_1,day_1)
    if check_data==True:
        print("Some Wrong Data Inputed!....Try again!")
        print("--------------------------------------------------------")
        main()
        
    elif check_data==False:
        return (city_1, month_1,day_1)
        print('-' * 40)


def check_valid(m,d):
    m=m.lower()
    d=d.lower()
    flag_month=True
    flag_day=True
    if m in months:
        flag_month=False
    if d in days_list:
        flag_day=False
    if flag_day==False and flag_month==False:
        return False
    else:
        return True


def load_data(city, month, day):
    """
       Loads data for the specified city and filters by month and day if applicable.

       Args:
           (str) city - name of the city to analyze
           (str) month - name of the month to filter by, or "all" to apply no month filter
           (str) day - name of the day of week to filter by, or "all" to apply no day filter
       Returns:
           df - pandas DataFrame containing city data filtered by month and day
       """
    try:
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name

    except (ValueError,UnboundLocalError,KeyError):
        print(" \nSeems Like You Inputed A Wrong City!....")
        main()

    if month != 'all':
        month = months.index(month) + 1
        df = df.loc[df['month'] == month]
        get_filters()

    if day != 'all':
        day = str(day).title()
        df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """    Displays statistics on the most frequent times of travel.

            Args: df(The filtered Data Frame)


              returns: most frequent time

    """
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    a=df['month'].value_counts()
    a=a.idxmax()
    a=int(a)
    print("The Most Common Month To Travel: {} With A Count Of: {} ".format(months[a-1],df['month'].value_counts().max()))
    n = pd.to_datetime(df['Start Time'])
    week = n.dt.weekday_name
    print("The Most Popular Day to Travel is: {} With A Count Of: {} ".format(week.value_counts().idxmax(),week.value_counts().max()))
    most_pop_series = (n.dt.hour).value_counts()
    print("The Most Popular Hour To Travel is: {}:00 With A Count Of: {}".format(most_pop_series.idxmax(),most_pop_series.max()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

         Args: df(The filtered Data Frame)


            returns: most popular stations and trip.

    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    c = df['Start Station']
    tot = (c.value_counts().idxmax())
    print("Most Common Start Station: {} With A Count Of: {} ".format(tot,c.value_counts().max()))
    d = df['End Station']
    tot_1 = (d.value_counts().idxmax())
    print("Most Common End Station: {} With A Count Of: {}  ".format(tot_1,d.value_counts().max()))
    b = df.groupby(['Start Station', 'End Station'])
    k = b.size()
    print("Most Popular Start Station And End Station is {} with a count {} ".format(k.idxmax(),k.max()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

       Args: df(The filtered Data Frame)


            returns: the total and average trip duration.

    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    m = df['Trip Duration']
    hours = (m.sum()) / 60
    minutes = (m.sum()) % 60
    mean = (m.mean())
    hours_1 = mean / 60
    minutes_1 = mean % 60
    print("Total Travel Time Is {} Hours And {} Minutes".format(hours, minutes))
    print("Mean travel Time Is {} Hours and {} Minutes".format(hours_1, minutes))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users.

          Args: df(The filtered Data Frame)


            returns: the statistics on bikeshare users.

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    k = df['User Type']
    print(k.value_counts())
    try:
        l = df['Gender']
        print(l.value_counts())
        m = df['Birth Year']
        m = m.fillna(method='backfill')
        print("The Youngest Birth Year: {}".format(m.max()))
        print("The Oldest Birth Year: {}".format(m.min()))
        print("The Most Popular Birth Year: {}".format(m.value_counts().idxmax()))
    except KeyError:
        print("This City Has NO Gender Data! ")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            exit(0)


if __name__ == "__main__":
	main()

