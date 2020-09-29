# Exploring-COVID
My work with the JHU CSSE COVID-19 Data which can be found at https://github.com/CSSEGISandData/COVID-19.

If you want to dowload and use this code yourself, I would suggest looking into how the data is formatted and structrured in their repository.

I am interested in looking at trends within the US, so I have focused the functionality of my code on just the US Daily Report files.

The get_COVID_df() function is used to scrape the csv files from the repository and make one comprehensive DataFrame for a variable of interest (i.e. get all the 'Confirmed' data (confirmed cases reported) for every State/Province on each day.

The get_delta_df() function returns a new DataFrame containing the differences between the rows of the given DataFrame. This will be helpful for looking at daily changes.

The get_two_weeks() function returns a new DataFrame containing data for a specific date as well as data for the dates two weeks before and two weeks after. This will be helpful when looking at trends before and after legislation and actions are taken by a state.
