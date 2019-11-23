# ---------------------------------------------------------------------------
# Parse and wrangle data
# ---------------------------------------------------------------------------

import pandas as pd

# Takes column of assignee names, returns df with assignee names and how
# many times they appear (sorted by num of appearances) + percentage
def getTopAssignees(names):

    # Get number of occurrences for each name
    count_names = {}
    for name in names:
        
        if name not in count_names:
            count_names[name] = 1
        else:
            count_names[name] = count_names[name] + 1
    
    # Get percentage of appearances for each name
    total_names = len(count_names)
    for name in count_names:
        pass


def main():
    df = pd.read_csv('scraped_patents.csv')
    getTopAssignees(df.loc[:, 'Assignee Name'])
    


main()