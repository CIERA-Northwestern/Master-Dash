'''This page is a template for creating a customized page with multiple panels.
This page deliberately avoids using too many functions to make it easier to
understand how to use streamlit.
'''
# Computation imports
import copy
import importlib
import os
import types
import datetime

import streamlit as st
import pandas as pd

from .. import dash_builder, utils

importlib.reload(dash_builder)


#### Developer Note:
# sorry if the code is messy :/
# we're trying to clean it up

def main(root:str,user_utils: types.ModuleType = None):
    '''This is the main function that runs the dashboard.

    Args:
        config_fp: The filepath to the configuration file.
        user_utils: The module containing the user-defined functions.
            Defaults to those in root_dash_lib.
    '''
    
    pd.options.mode.copy_on_write = True
    # This must be the first streamlit command
    st.set_page_config(layout='wide')
    st.title("the master dash")
    st.subheader("outreach -- events -- visits -- press")

    # DASHBOARD SPECIFICATION
    # user choice on which dashboard to view
    # as well as where to source data from (manual entry or latest stored csv)
    #######################################################################################


    data_provided = False
    with st.container(border=True):
        datasource = st.radio("where to source the data?",
                 ["manual entry", "latest stored csv"], index=None)
        st.text("manual data entry will attempt to automatically match the data provided to the specific dashboard by column name\nto view the latest stored csv, you must choose desired dash.")
        if datasource == "manual entry":
            datapattern = st.file_uploader("drag-and-drop your csv file")
            
            #### Developer Note:
            # if you select manual entry, then we automatically match the provided csv with dashboard options
            # by pattern matching on the column titles
            # IF YOU ARE GOING TO MODIFY COLUMN TITLES, please change it here.
            # it needs to be an exact match in order to pair, so even one column off will raise errors
            # also, make sure the column titles are on the first row of the csv.
            if datapattern is not None:
                ind = -1


                # by index: event:0, press:1, visits:2, outreach:3
                dash_patterns = [b'Calendar Group,Event Type Tags,id,Title,Category,Research Topic,Date,Duration,Attendance,Location,Year\n',
                                 b'id,Title,Date,Permalink,Research Topics,Press Types,Categories,Press Mentions,People Reached,Top Outlets,,\r\n',
                                 b'id,Name,"Visitor Institution",ciera_visit_international,"Post Date",Host,"Host Types",Content,Permalink,"Start Date (UnixTimestamp -- date=(((UnixTimeStamp/60)/60)/24)+DATE(1970,1,1))","End Date (UnixTimestamp)","Academic Year (as defined on website backend = FY-1)",Programs,Tags\n',
                                 b',,,Basic Info,,,,"Names of CIERA volunteers\r\n']
                dash_cols = datapattern.readline()
                print(dash_cols)
                if dash_cols in dash_patterns:
                    ind = dash_patterns.index(dash_cols)

                if ind == -1:
                    st.text('Something went wrong; input data not recognized\nplease consult the manual for correct data formatting')
                    data_provided = False
                else:
                    data_provided = True
                    reverse_map = {0:'events', 1:'press', 2:'visits', 3:'outreach'}
                    dashkey = reverse_map[ind]
                    # this just gets the pointer back to the start of the csv
                    datapattern.seek(0, 0)



        elif datasource == 'latest stored csv':
            datapattern = None
            data_provided = True

            dashkey = st.selectbox('select your dashboard to view', ['press', 'events', 'visits', 'outreach'], )
            map = {'press':1, 'events':0, 'visits':2, 'outreach':3}
            ind = map[dashkey]

    #######################################################################################
    # At this point, you have sourced a csv to view, or selected the appropriate dashboard


    # Prep data
    if data_provided:
        # get the correct config file
        config_dir = root
        config_fn = f'{dashkey}_configs.yml'
        config_fp =  os.path.join(config_dir, config_fn)

         # Get the builder used to construct the dashboard
        builder = dash_builder.DashBuilder(config_fp=config_fp, dash_ind=ind)

        # Set the title that shows up at the top of the dashboard
        st.title(builder.config.get('page_title','Dashboard'))
        
        data, config = builder.prep_data(builder.config,dataset=datapattern)
        builder.config.update(config)

        # Global settings
        st.sidebar.markdown('# Data Settings')
        setting_check = builder.interface.request_data_settings(st.sidebar)

        st.sidebar.markdown('# View Settings')
        builder.interface.request_view_settings(st.sidebar)

        # got rid of the data recategorization function
        # because it doesnt really match our goals for this dataset
        # all the infrastructure is still there though
        # if you would like to re-add, uncomment relevant sections in
        # base_page, interface, and data_handler
        selected_settings = builder.settings.common['data']
        '''data['recategorized'] = builder.recategorize_data(
            preprocessed_df=data['preprocessed'],
            new_categories=builder.config.get('new_categories', {}),
            recategorize=selected_settings['recategorize'],
            combine_single_categories=selected_settings.get(
                'combine_single_categories',
                False
            ),
        )'''

        ### Note:
        # for future reference, if you want to set artificial bounds for year/timescale, do it here
        min_year = int(data['preprocessed']['Date'].dt.year.min())
        max_year = int(data['preprocessed']['Date'].dt.year.max())
        
    
        # Data axes
        # entered search category passed down to filter settings for further specification
        st.subheader('Data Axes')    
        st.text("Note: entries from before Jan 1st, 2014 are classified as LEGACY for the purposes of data categorization")

        axes_object = builder.interface.request_data_axes(st, max_year, min_year)
        #print(axes_object)

        # filters data as per specs
        # the specific interface used in filtering is determined with the choice of dashboard
        temp_data, selecset = builder.interface.process_filter_settings(
            st,
            data['preprocessed'],
            value=builder.settings.get_settings(common_to_include=['data'])['groupby_column'],
        )
        #print(builder.settings.common['data'])

        # Apply data filters
        data['selected'] = builder.filter_data(
            temp_data,
            builder.settings.common['filters'],
        )

        
        # TIME BOUNDING
        # here, we bound the dashboard view by years/month specified by user
        # all entries not falling into this bound are not shown
        #######################################################################################
        
        
        reverse_month_dict = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May',6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

        # extracts time information from axes_object
        # i.e. when to start the year (by month) and year bounds
        time_object = axes_object['x_column'].split(':')
        month_start = int(time_object[1])
        year_start = int(time_object[2])
        year_end = int(time_object[3])
        years_to_display = list(range(year_start+1, year_end+1))

        # redefines the year in terms of the user month start
        # here is where you might outline fiscal year definitions (year starts in september) for example
        month_redef = [x if x<=12 else x-12 for x in range(month_start, 12+month_start)]
        defdate = datetime.date(min_year, 1, 1)

        # gets the year of each entry in terms of the user specified period
        # e.g. if an entry was registered in october of 2025, but you are selecting based in fiscal year
        # the entry would have reindex year 2026 
        data['selected']['Reindexed Year'] = utils.get_year(
                data['selected']['Date'], "{} 1".format(reverse_month_dict[month_start]),
                default_date_start=min_year,
                default_date_end=max_year
            )
        
        ######## 
        ## here, we construct the actual time-bounded dataset, 'windowed'
        ## I'm sure we could have done this in a better way, but as it stands, we first start by mapping all of the beginning year
        # of the period's entries to the new dataset; then, we concatenate all relevant subsequent years
        # its clunky, I know. but it should work (if you want to make a better version, be my guest)
        data['windowed'] = data['selected'][data['selected']['Reindexed Year'] == year_start]

        ## above is the case if we have greater than one year selected
        if len(years_to_display) != 0:
            for i in years_to_display:
                temp = data['selected'][data['selected']['Reindexed Year'] == i]
                data['windowed'] = pd.concat([data['windowed'], temp])

            builder.settings.common['data']['x_column'] = 'Reindexed Year'

        ### if no/one year is selected, i.e. if start year and end year are the same on slider,
        # then we automatically break down into the month-by-month display for that year
        # this entails decomposing that year's entries to month-by-month binning, while
        # still taking into account user's desired start month
        if len(years_to_display) == 0:

            # For Fiscal Month visualizations
            def month_fisc_converter(month:int, forward=True):
                return month_redef.index(month)+1
            
            # set 'reindexed month' to the result of month_fisc_converter
            data['windowed'].loc.__setitem__((slice(None), 'Reindexed Month'), data['windowed'].__getitem__('Date').dt.month.map(month_fisc_converter))
            builder.settings.common['data']['x_column'] = 'Reindexed Month'
            
            # extract real month, just to have
            def month_extractor(month):
                return reverse_month_dict[int(month)]
            data['windowed']['Calendar Month'] = data['windowed']['Date'].dt.month.apply(month_extractor)

        ### if no entries fall into this time window, we instantiate the whole graph with zeroes,
        # just for, like, normalization/regularization purposes going forward
        # so other stuff doesn't completely freak out
        if data['windowed'].empty:
            locd = {}
            for i in data['windowed'].columns:
                locd[i] = "normalization value; ignore for data purposes"
            data['windowed'].loc[0] = locd
    
        #######################################################################################       
    
    
        # Here, we make a human-readable final datasheet by collapsing the exploded entries back into single, by unique entry id
        data['final'] = data['preprocessed'].filter(items=set(data['windowed'].index), axis=0)
    
        #print(builder.settings.common)
        time_class = builder.settings.common['data']['x_column']
        
        # Aggregate data

        ###
        data['totals'] = builder.aggregate(
            data['windowed'],
            ('Calendar Month' if time_class == "Reindexed Month" else time_class),
            builder.settings.common['data']['y_column'],
            aggregation_method=builder.settings.common['data']['aggregation_method'],
        )
        
        # Aggregate data
        
        data['aggregated'] = builder.aggregate(
                data['windowed'],
                ('Calendar Month' if time_class == "Reindexed Month" else time_class),
                builder.settings.common['data']['y_column'],
                builder.settings.common['data']['groupby_column'],
                builder.settings.common['data']['aggregation_method'],
        )
        
        ##### AGGREGATION REFINING
        # while we are declaring the 'aggregated' and 'total' datasets by above,
        # that simple instantiation has a number of issues
        # we solve those below, by kind of reinstantiating it?
        # the key idea for below is going from a sparse dataframe (above) to a dense dataframe, which we want for display purposes
        # it all works, as of 09/19/25
        #######################################################################################
        
        temp = data['aggregated'].sum()
        data['total by instance'] = pd.DataFrame(index = temp.index, data={'Aggregate': temp.values})
        data['total by instance'].sort_values(ascending=False, by='Aggregate', inplace=True)
        
        ### adds all years for which we have data back into aggregated dataframe (even if all zero that time bin);
        # more accurately displays trends across multiple years
        years_to_display.insert(0, year_start)
        
        # If you are going to change the configs for x_columns, make sure they are reflected below!


        ## essentially, how this works is we make sure that years without any data entries are still represented in aggregated and totals graphs
        # we construct a new, dense, dataframe and set the aggregated and total to that
        if len(list(data['aggregated'].columns)) != 0:

            data['aggregated'] = data['aggregated'].T
            data['totals'] = data['totals'].T
    
            if time_class == 'Reindexed Month':
                xaxis = [reverse_month_dict[i] for i in month_redef]
            elif time_class == 'Reindexed Year':
                xaxis = years_to_display
            
            yaxis = pd.unique(data['selected'][builder.settings.common['data']['groupby_column']]) 
            datumx = {}
            for x in xaxis:
                datumy = {}
                if x in data['aggregated'].columns:
                    for y in yaxis:
                        if y in data['aggregated'].index:
                            datumy[y] = int(getattr(data['aggregated'][x], y, 0))
                        else:
                            datumy[y] = 0
                else:
                    for y in yaxis:
                        datumy[y] = 0
                datumx[str(x)] = datumy

            aggregatee = pd.DataFrame(data = datumx)
            data['aggregated'] = aggregatee

            totalx = {}
            for x in xaxis:
                if x in data['totals'].columns:
                    totalx[x] = int(getattr(data['totals'][x], builder.settings.common['data']['y_column'], 0))
                else:
                    totalx[x] = 0    
            totalee = pd.Series(data=totalx)
            data['totals'] = totalee
            ###

            data['aggregated'] = data['aggregated'].T
            #data['totals'] = data['totals'].T

        else:
            datumx = {}
            for i in range(1, 13):
                datumy = {}
                for j in data['windowed'].columns:
                    datumy[j] = 0
                datumx[i] = datumy
            aggregatee = pd.DataFrame(datumx)

            totalx = {}
            for i in range(1, 13):
                totalx[i] = 0
            totalee = pd.Series(data = totalx)
            data['totals'] = totalee

            data['aggregated'] = aggregatee.T
        
        #######################################################################################

        # adds NaN values to dataframe for viewing
        if 'categorical' in builder.settings.common['filters']:
            for topic in builder.settings.common['filters']['categorical'][builder.settings.get_settings(common_to_include=['data'])['groupby_column']]:
                if topic not in data['aggregated'].columns:
                    data['aggregated'][topic] = [0 for i in range(len(data['aggregated'].index))]

        

        st.header('Data Plotting')
        st.text("Note: data entries may correspond to multiple categories, and so be represented in each grouping")
        st.text("please be cognizant of this; an accurate count of all entries is provided by 'total' option in data settings")


        ### Developer Note:
        # this is view stuff; the legacy view options using the 'lineplot' view are left in place, if you want to mess with them
        # however, we mainly use the 'testplot' option, as it is more flexible and uses plotly.

        # Lineplot IF data option is total or none
        data_option = builder.settings.common['data']['data_options']
        if data_option in ['No Total', 'Only Total', 'Standard']:
            local_key = 'lineplot'
            st.subheader('Line Plot Visualization')
            '''        
            with st.expander('Lineplot settings'):
                local_opt_keys, common_opt_keys, unset_opt_keys = builder.settings.get_local_global_and_unset(
                    function=builder.data_viewer.lineplot,
                )
                builder.interface.request_view_settings(
                        st,
                        ask_for=unset_opt_keys,
                        local_key=local_key,
                        selected_settings=builder.settings.local.setdefault('lineplot', {}),
                        tag=local_key,
                        default_x=builder.settings.common['data']['x_column'],
                        default_y=builder.settings.common['data']['y_column'],
                )
                local_opt_keys, common_opt_keys, unset_opt_keys = builder.settings.get_local_global_and_unset(
                    function = builder.data_viewer.lineplot,
                    local_key=local_key,
                )
            '''
        #constructs line plot based on specifications provided
            if data_option == "No Total":
                builder.data_viewer.testplot(
                    df = data['aggregated'],
                    month_reindex = month_redef if builder.settings.common['data']['x_column_ind'] == 0 else None, 
                    year_reindex = years_to_display,
                    y_label=builder.settings.common['data']['y_column'],
                    x_label=builder.settings.common['data']['x_column'],
                    category=builder.settings.common['data']['groupby_column'],
                    view_mode=builder.settings.common['view']['view_mode']
                )
            elif data_option == "Only Total":
                builder.data_viewer.testplot(
                    df = data['totals'].to_frame(name="totals"),
                    month_reindex = month_redef if builder.settings.common['data']['x_column_ind'] == 0 else None, 
                    year_reindex=years_to_display,
                    y_label=builder.settings.common['data']['y_column'],
                    x_label=builder.settings.common['data']['x_column'],
                    category=builder.settings.common['data']['groupby_column'],
                    view_mode=builder.settings.common['view']['view_mode']
                    #**builder.settings.get_settings(local_key)
                )
            elif data_option == "Standard":
                builder.data_viewer.testplot(
                    df = data['aggregated'],
                    month_reindex = month_redef if builder.settings.common['data']['x_column_ind'] == 0 else None, 
                    year_reindex = years_to_display,
                    totals = data['totals'],
                    y_label=builder.settings.common['data']['y_column'],
                    x_label=builder.settings.common['data']['x_column'],
                    category=builder.settings.common['data']['groupby_column'],
                    view_mode=builder.settings.common['view']['view_mode']
                )
        # Bar Plot IF data option is aggregated
        elif data_option == "Year Aggregate":
            #print(data['total_by_instance'].columns)
            st.subheader('Bar Plot Visualization')
            builder.data_viewer.barplot(
                data['total by instance'],
            )
        '''
        elif data_option == "testing":
            st.subheader("testing chart; please disregard")
            builder.data_viewer.testplot(
                df = data['aggregated'],
                month_reindex = month_redef if builder.settings.common['data']['x_column_ind'] == 0 else None, 
                year_reindex = years_to_display,
                totals = data['totals'],
                y_label=builder.settings.common['data']['y_column'],
                x_label=builder.settings.common['data']['x_column'],
                category=builder.settings.common['data']['groupby_column']
            )
        '''
        # View the data directly
        builder.data_viewer.write(data)
