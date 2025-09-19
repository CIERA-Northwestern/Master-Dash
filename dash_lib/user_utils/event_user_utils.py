'''Functions for loading and preprocessing the data, specific to
the user's data. If you are adapting the dashboard as your own,
you likely need to alter these functions.
'''
import os
import glob
import numpy as np
import pandas as pd

from dash_lib import utils


def load_data(data, config):
    '''Modify this!
    
    This is the main function for loading the data
    (but save cleaning and preprocessing for later).
    
    For compatibility with the existing
    dashboard, this function should accept a pandas DataFrame and a
    config dictionary and return the same.

    Args:
        config (dict): The configuration dictionary, loaded from a YAML file.

    Returns:
        raw_df (pandas.DataFrame): The data to be used in the dashboard.
        config (dict): The configuration dictionary, loaded from a YAML file.
    '''

    ##########################################################################
    # Filepaths
    if data is None:
        input_dir = os.path.join(config['data_dir'], config['input_dirname'])

        def get_fp_of_most_recent_file(pattern):
            '''Get the filepath of the most-recently created file matching
            the pattern. We just define this here because we use it twice.

            Args:
                pattern (str): The pattern to match.

            Returns:
                fp (str): The filepath of the most-recently created file
                    matching the pattern.
            '''
            fps = glob.glob(pattern)
            ind_selected = np.argmax([os.path.getctime(_) for _ in fps])
            return fps[ind_selected]

        data_pattern = os.path.join(input_dir, config['website_data_file_pattern'])
        data_fp = get_fp_of_most_recent_file(data_pattern)
    else:
        data_fp = data

    ##########################################################################
    # Load data

    # Website data
    #os.chdir(os.path.dirname(os.path.abspath(__file__)))
    website_df = pd.read_csv(data_fp, encoding_errors='ignore')
    #website_df['id'] = website_df.index
    website_df.set_index(np.arange(len(website_df)), inplace=True)
    #website_df.set_index('Calendar Group', inplace=True)

    #testing
    
    # website_df = pd.read_csv(data_fp, parse_dates=['Date',])
    # website_df.set_index('id', inplace=True)
    
    # # Load press data
    # press_df = pd.read_excel(press_office_data_fp)
    # press_df.set_index('id', inplace=True)

    # # Combine the data
    # raw_df = website_df.join(press_df)

    return website_df, config


def clean_data(raw_df, config):
    '''Modify this!
    
    This is the main function for cleaning the data,
    i.e. getting rid of NaNs, dropping glitches, etc.
    
    For compatibility with the existing
    dashboard, this function should accept a pandas DataFrame and a
    config dictionary and return the same.

    Args:
        raw_df (pandas.DataFrame): The raw data to be used in the dashboard.
        config (dict): The configuration dictionary, loaded from a YAML file.

    Returns:
        cleaned_df (pandas.DataFrame): The cleaned data.
        config (dict): The (possibly altered) configuration dictionary.
    '''

    print(raw_df.columns)

    # Drop rows where 'Date' year is 1970
    cleaned_df = raw_df[raw_df['Date'] != 0]
    
    # # Drop drafts
    # cleaned_df = raw_df.drop(
    #     raw_df.index[raw_df['Date'].dt.year == 1970],
    #     axis='rows',
    # )

    

    # Drop weird articles---ancient ones w/o a title or year
    cleaned_df.dropna(
        axis='rows',
        how='any',
        subset=['Title', 'Date', 'Calendar Group', 'Event Type Tags'],  
        inplace=True,
    )
    
    #Calendar Group,Event Type Tags,id,Title,Category,Research Topic,Date,Attendance,Location,Year


    # Get rid of HTML ampersands
    for str_column in ['Event Type Tags', 'Title', 'Category', 'Research Topic','Location']:
        cleaned_df[str_column] = cleaned_df[str_column].str.replace('&amp;', '&')

    # Handle NaNs and such

    AVERAGE_NUM_ATTENDEES = 10
    def resolve_numerical(entry):
        try:
            entry = int(entry)
        except:
            entry = AVERAGE_NUM_ATTENDEES
        
        return entry
        
    cleaned_df['Attendance'] = cleaned_df['Attendance'].apply(resolve_numerical)
    cleaned_df.fillna(value='N/A', inplace=True)

    return cleaned_df, config


def preprocess_data(cleaned_df, config):
    '''Modify this!
    
    This is the main function for doing preprocessing, e.g. 
    adding new columns, renaming them, etc.
    
    For compatibility with the existing
    dashboard, this function should accept a pandas DataFrame and a
    config dictionary and return the same.

    Args:
        cleaned_df (pandas.DataFrame): The raw data to be used in the dashboard.
        config (dict): The configuration dictionary, loaded from a YAML file.

    Returns:
        processed_df (pandas.DataFrame): The processed data.
        config (dict): The (possibly altered) configuration dictionary.
    '''

    preprocessed_df = cleaned_df.copy()
    '''
    # Get the year, according to the config start date
    preprocessed_df['Fiscal Year'] = utils.get_year(
        preprocessed_df['Date'], config['start_of_year']
    )
    
    preprocessed_df['Calendar Year'] = preprocessed_df['Date'].dt.year

    # Tweaks to the press data
    #if 'Title (optional)' in preprocessed_df.columns:
    #    preprocessed_df.drop('Title (optional)', axis='columns', inplace=True)
    #for column in ['Year']:
    #    preprocessed_df[column] = preprocessed_df[column].astype('Int64')    

    # Now explode the data
    for group_by_i in config['groupings']:
        preprocessed_df[group_by_i] = preprocessed_df[group_by_i].str.split('|')
        preprocessed_df = preprocessed_df.explode(group_by_i)

    # Exploding the data results in duplicate IDs,
    # so let's set up some new, unique IDs.
    '''
    preprocessed_df['Date'] = pd.to_datetime(preprocessed_df['Date'], errors='coerce')
    
    preprocessed_df['id'] = preprocessed_df.index
    preprocessed_df.set_index(np.arange(len(preprocessed_df)), inplace=True)


    ### Developer Note: 'legacy' is a CIERA specified field which delineates all data into
    # current vs legacy bins, with the latter being defined as all entries before 2014
    # this was done at the request of operations director Kari Frank
    # best to keep it
    def legacy(date):
        if date.year < 2014:
            return "LEGACY"
        else:
            return "CURRENT"
    
    preprocessed_df['Legacy'] = preprocessed_df['Date'].apply(legacy)



    # This flag exists just to demonstrate you can modify the config
    # during the user functions
    config['data_preprocessed'] = True

    return preprocessed_df, config
