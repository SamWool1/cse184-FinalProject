# ---------------------------------------------------------------------------
# Parse and wrangle data
# ---------------------------------------------------------------------------

import pandas as pd
import numpy as np
import datetime

# Creates a single spreadsheet with values for all years
def createUnifiedScrape():
    unified_df = pd.DataFrame()
    for year in range(1980, 2019):
        year = str(year)
        df = pd.read_csv('scrapes/scraped_patents' + year + '.csv')
        df['Year'] = year
        unified_df = unified_df.append(df)
    print(unified_df.head())
    unified_df.to_csv('unified_patents.csv')

# Get a count and percentage of unique values in a column
def getCountAndPercent(values):

    # Get number of occurrences for each value
    count_values = {}
    for value in values:
        value = str(value).upper()

        if value not in count_values:
            count_values[value] = 1
        else:
            count_values[value] = count_values[value] + 1

    # Craete dataframe and get percentage of appearances for each value
    total_count = len(values)
    df = pd.DataFrame(columns=np.arange(3))
    df.columns = ['Value', 'Count', 'Percentage']

    for i, value in enumerate(count_values):
        count = count_values[value]
        percentage = count/total_count
        df.loc[i] = [value, count, percentage]

    return df


# TODO remove, for testing date-time delta stuff
def test_func(df):
    dates = df.loc[:, 'Patent Date']
    for date_str in dates:
        try:
            date = datetime.datetime.strptime(date_str, '%B %d, %Y')
            print(date)
        except Exception:
            print('Unknown')
    return


def main(year):
    df = pd.read_csv('scrapes/scraped_patents' + year + '.csv')
    df.dropna(subset=['Assignee Name'], inplace=True)

    assignee_name_df = getCountAndPercent(df.loc[:, 'Assignee Name'])
    print(assignee_name_df.sort_values('Count', ascending=False).head())

    place_df = getCountAndPercent(df.loc[:, 'Assignee Location'])
    print(place_df.sort_values('Count', ascending=False))

    # test_func(df)


createUnifiedScrape()
# for year in range(1980, 2019):
#     print('Wrangling ' + str(year))
#     main(str(year))
#     input('Finished ' + str(year) + ', press Enter to continue...')
# print('All wrangling finished')
