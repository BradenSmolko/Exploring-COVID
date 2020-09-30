import datetime as dt
import pandas as pd


def get_COVID_df(column_of_interest = 'Incident_Rate', dropna = False):
    '''
    Function to return a DataFrame of the aggregated data accross the US Daily
    Reports for a particular column of interest.
    
    Parameters
    ----------
    column_of_interest : String, optional
        The column of interest to aggregate from the daily reports.
        The default is 'Incident_Rate'.
        Other options include:
            - 'Confirmed'
            - 'Deaths'
            - 'Recovered'
            - 'Active'
            - 'People_Tested'
            - 'People_Hospitalized'
            - 'Mortality_Rate'
            
    dropna : Boolean, optional
        Drops States/Provinces that have rows with NaN values. The default is False.

    Returns
    -------
    df : Pandas DataFrame object
        The DataFrame object contains the column of interest from all dates and
        states/provinces.

    '''
    # Get dates ranging from the start of daily reports to current day
    dt_objects = pd.date_range('04/12/2020', dt.datetime.today())
    
    # Put dates in format of the file names
    dates = []
    for dt_obj in dt_objects:
        dates.append(dt_obj.strftime("%m-%d-%Y"))
        
    # Iterate over the csv files in the csse_covid_19_daily_reports_us branch to get the state 
    # and the column of interest. Add all of these dfs to a list to iterate over later.
    list_of_dfs = []
    
    for date in dates:
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{}.csv'.format(date)
        try: 
            df = pd.read_csv(url)
            df = df[['Province_State', column_of_interest]]
            df.set_index('Province_State', inplace = True)
            df.columns = [date]
            list_of_dfs.append(df)
        except:
            pass
    
    # Iterate over the dfs and join them on State/Province
    df = list_of_dfs[0]
    for dat in list_of_dfs[1:]:
        df = df.join(dat, on = 'Province_State')
    
    # If dropna is True, drop rows with NaN values
    if dropna:
        df = df.dropna()
    
    # Transpose the df and name index ('Date')
    df = df.transpose()
    df.index.name = 'Date'
    
    return df


# You may want to see the changes accross the days for each state (removes day 1)
def get_delta_df(data):
    '''
    Returns a Pandas DataFrame object that consists of the change between rows
    of the given DataFrame. 
    
    i.e. the row of data for 05/21/2020 in the resulting DataFrame is equivalent
    to the values from 05/21/2020 - 05/20/2020 of the given DataFrame. It shows
    the observed change on that day compared to the previous.

    Parameters
    ----------
    data : Pandas DataFrame object
        DataFrame of numerical values.

    Returns
    -------
    Pandas DataFrame object
        DataFrame with the differences of every row calculated. The first row is
        dropped from the given DataFrame as there is no data before it. This means
        that the resulting DataFrame will contain one less row.

    '''
    return data.diff().iloc[1:,:]


# Get a df of the values of cases at a specified date, two weeks before, two weeks after
def get_two_weeks(data, date = dt.datetime.today().strftime("%m/%d/%Y")):
    '''
    Get the values of data from the given DataFrame for the date specified, the
    date two weeks before, and the date two weeks after. This is to help see
    changes in cases that may be caused by events or legislation. Due to the
    nature of the COVID-19 disease, impacts of these events are not visible
    immediately in the numbers. Those infected may take up to two weeks to show
    symptoms. If data not available for the dates, a message will be printed.
    In the resulting DataFrame, the values of the next day and the day previous 
    have been averaged together. This is to help combat the high daily 
    fluctuation seen in the data.

    Parameters
    ----------
    data : Pandas DataFrame object
        A DataFrame object storing data with a date index.
    date : STRING
        A string representing a date in the format of 'mm/dd/YYYY'.
        The default is dt.datetime.today().strftime("%m-%d-%Y"). AKA 'Today's date'

    Returns
    -------
    df : Pandas DataFrame object
        Returns a DataFrame object with at most 3 rows from the given DataFrame.
        These rows will consist of data averaged from the date two weeks before 
        the one specified plus and minus a day, the averaged data for date specified
        plus or minus a day, and the averaged data for the date two weeks after the 
        one specified plus and minus a day.

    '''
    date = dt.datetime.strptime(date, '%m/%d/%Y')
    # Calculate and format the dates
    two_weeks = dt.timedelta(14)
    one_day = dt.timedelta(1)
    
    date_before = date - two_weeks
    date_after = date + two_weeks
    
    dates_before = [date_before - one_day, date_before, date_before + one_day]
    dates_interest = [date - one_day, date, date + one_day]
    dates_after = [date_after - one_day, date_after, date_after + one_day]
    
    dates = [dates_before, dates_interest, dates_after]
    
    for collection in dates:
    	for i, dt_obj in enumerate(collection):
    		collection[i] = dt_obj.strftime("%m-%d-%Y")
    
    # Get the appropriate rows if they exist
    df = pd.DataFrame()
    new_index = []
    for collection in dates:
        try:
            df = df.append(data.loc[collection,].mean(),ignore_index = True)
            new_index.append(str(collection[1]))
        except:
            print("Insufficient data for {}".format(collection[1]))
    df.index = new_index
    df.index.name = 'Values Averaged Around Day'
    return df

