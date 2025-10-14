# CIERA MASTER Dashboard
This dashboard provides a way for interested individuals to explore data regarding four key CIERA metrics:
1. Press
2. Events
3. Outreach
4. Visits

Instructions are provided below for various levels of usage.
Even if you have never edited code before, the goal of the instructions in [Level 2](#level-2-using-the-dashboard-on-your-computer) is for you to run the dashboard on your computer.
On the other end of things, if you are comfortable with routine use of git, code testing, etc., then jump to [Level 4](#level-4-significant-customization-and-editing) to get an overview of how the dashboard works and what you might want to edit.
To update the dashboard, jump to [Level 1](#level-1-updating-the-configuration-and-data): Updating the Configuration and Data .

## Table of Contents

- [Level 0: Using the Dashboard Online](#level-0-using-the-dashboard-online)
- [Level 1: Updating the Configuration and Data](#level-1-updating-the-configuration-and-data)
- [Level 2: Using the Dashboard on your Computer](#level-2-using-the-dashboard-on-your-computer)
- [Level 3: Making Some Edits to the Code](#level-3-making-some-edits-to-the-code)
- [Level 4: Significant Customization and Editing](#level-4-significant-customization-and-editing)

## Level 0: Using the Dashboard Online

The dashboard has a plethora of features that can be interacted with via a web interface.
If the dashboard is currently live at [master-dash](https://the-master-dash.streamlit.app/), you can use the dashboard without any additional effort.

## Level 1: Updating the Configuration and Data

When the dashboard is hosted on the web in some cases you can edit the configuration and data without ever needing to download anything and view the updated dashboard without ever needing to download anything.
This is possible for dashboards where the computations are sufficiently light to be wrapped into the interactive dashboard.

### Editing the Configs


The dashboard incorporates a series of config files (corresponding to each focus area; outreach, visits, press and events) to provide for surface-level customization. These files are found in the the root directory, i.e. [here](https://github.com/CIERA-Northwestern/Master-Dash).
You can edit this on github by clicking on the edit button in the upper right, provided you are logged in with an account that has the necessary permissions.
Locally this can be edited with TextEdit (mac), Notepad (Windows), or your favorite code editor.
Keep in mind, these files are intended to provide a very light degree of configuration - in all likelihood, significant changes will require deeper work.

### Updating and Viewing the Data

There are two ways to update data on the dashboard. 
1. ***In-Dashboard Manual Upload***: to view data quickly and easily, we provide an option for in-dashboard data modification, process for which is outlined below. Please be advised that this method of visualization is NON-PERSISTENT: data input is not stored for later use; if you exit out of the master-dash, you will have to reupload.
   1. Boot up the dashboard, as usual.
   2. Select the 'Manual Entry' toggle in the startup prompt
   3. Drag-and-Drop your updated csv into the provided space
      1. master-dashboard should automatically match/identify which sub-metric to display from column names of csv - DO NOT REMOVE THEM
   4. View data as normal    
2. ***Github Persistent Upload***: for cases when PERSISTENT storage is desired, we provide direct users to the specific repo for data.
   1. Navigate to the raw-data folder in master-dash github repo ([here](https://github.com/CIERA-Northwestern/Master-Dash/tree/main/data/raw_data)).
   2. Select 'add file' in the upper right corner of the page (opposite the directory name 'master-dash/tree/...'), then choose 'Upload Files'
   3. Drag-and-drop desired csv into slot as needed, ensuring that the file adheres to following naming conventions (necessary for pattern matching and file/pathing):
      1. Events: "events-live-***.csv" ( * can be anything)
      2. Press: "News_Report_Main_***.csv"
      3. Outreach: "Outreach_Data-***.csv"
      4. Visits: "Visits_Report-***.csv"
   4. If desired, provide an optional message to describe changes, then select the 'commit changes' option.
   5. This should bring the csv file into the pool for the master-dash to identify.
   6. Additionally, for record keeping, please move the previous iteration of the file updated into the Archived-data folder ([here](https://github.com/CIERA-Northwestern/Master-Dash/tree/main/data/archived_data)), by downloading a copy, deleting it from the raw-data folder, and uploading it to archived.
   7. In the dashboard, select the 'reload' option in the bottom right corner, to ensure the github integration is up to date. Then, select the 'latest stored csv' option in the prompt, and then choose desired submetric to view.

## Level 2: Using the Dashboard on your Computer

If you need a private dashboard or you need to run more-intensive data processing you'll need to run the dashboard on your computer.

### Downloading the Code

The code lives in a git repository, but you don't have to know git to retrieve and use it.
The process for downloading the code is as follows:

1. Click on the green "Code" button on [the GitHub repository](https://github.com/CIERA-Northwestern/Master-Dash), near the top of the page.
2. Select "Download ZIP."
3. Extract the downloaded ZIP file.

### Installing the Dashboard

Running the dashboard requires Python.
If you do not have Python on your computer it is recommended you download and install [Miniconda](https://docs.conda.io/en/main/miniconda.html).
Note that macs typically have a pre-existing Python installation, but this installation is not set up to install new packages easily, and the below instructions may not work.
Therefore it is still recommended that you install via miniconda even if your system has Python pre-installed.

Open the directory containing the code (the root directory) in your terminal or command prompt.
If youre a mac user and you've never used a terminal or command prompt before
you can do this by right clicking the extracted folder and selecting "New Terminal at Folder" ([more info](https://support.apple.com/guide/terminal/open-new-terminal-windows-and-tabs-trmlb20c7888/mac); [Windows Terminal is the windows equivalent](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands)).

Once inside the root directory and in a terminal, you can install the code by executing the command
```
pip install -e .
```

### Running the Dashboard Locally

Inside the root directory and in a terminal window, enter
```
streamlit run src/dashboard.py
```
This will open the dashboard in a tab in your default browser.
This does not require internet access.

### Running the Data Pipeline

To run the data-processing pipeline, while in the root directory run the following command in your terminal:
```
./src/pipeline.sh ./src/config.yml
```

### Viewing the Logs

Usage logs are automatically output to the `logs` directory.
You can open the notebooks as you would a normal Python notebook, if you are familiar with those.

## Level 3: Making Some Edits to the Code

### Downloading the Code (with git)

A basic familiarity with git is highly recommended if you intend to edit the code yourself.
There are many good tutorials available (e.g.
[GitHub's "Git Handbook"](https://guides.github.com/introduction/git-handbook/),
[Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials),
[Git - The Simple Guide](http://rogerdudler.github.io/git-guide/),
[Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)).
For convenience, the main command you need to download the code with git is
```
git clone git@github.com:CIERA-Northwestern/Master-Dash.git`
```

### Editing the Streamlit Script

The interactive dashboard is powered by [Streamlit](https://streamlit.io/), a Python library that enables easy interactive access.
Streamlit is built on a very simple idea---to make something interactive, just rerun the script every time the user makes a change.
This enables editing the streamlit script to be almost exactly like an ordinary Python script.
If you know how to make plots in Python, then you know how to make interactive plots with Streamlit.

If you want to change the Streamlit dashboard, edit `src/dashboard.py`.
Much of the Streamlit functionality is also encapsulated in utility functions inside the `press_dash_lib/` directory, particularly in `visit_dash_lib/streamlit_utils.py`.
Streamlit speeds up calculations by caching calls to functions.
If a particular combination of arguments has been passed to the function
(and the function is wrapped in the decorator `st.cache_data` or `st.cache_resource`)
then the results are stored in memory for easy access if the same arguments are passed again.

## Level 4: Significant Customization and Editing

Before making significant edits it is recommended you make your own fork of the dashboard repository,
and make your own edits as a branch. Additionally, if possible, keep edits largely localized to the 'dash_lib' folder [here](https://github.com/CIERA-Northwestern/Master-Dash/tree/main/dash_lib)
This will enable you to share your edits as a pull request.


### Code Structure
The dashboard is designed to be as streamlined as possible, meaning any potentially redundant files are merged, and we only exhibit multiple copies of a file if absolutely necessary. Practically, this has amounted to:

the central 'spine', consisting of:
1. the base page in [pages](https://github.com/CIERA-Northwestern/Master-Dash/tree/main/dash_lib/pages)
2. various pipeline and data processing files (such as aggregator or dash-builder, all located in dash_lib proper)

and metric specific offshoots
1. interfaces ([here](https://github.com/CIERA-Northwestern/Master-Dash/tree/main/dash_lib/interfaces)) control visual presentation/user options for each metric
2. user_utils ([here](https://github.com/CIERA-Northwestern/Master-Dash/tree/main/dash_lib/user_utils)) control metric-specific data preprocessing


KEEP IN MIND: any change to the spine is global to all dashboards, while changes to offshoots are local, only modifying specific metric behaviour

### Updating the Usage and Installation Instructions

If your edits include new packages, you need to add them to both `requirements.txt` and `setup.py`.
You may also consider changing the metadata in `setup.py`.

### Deploying on the Web
You can deploy your app on the web using Streamlit sharing.
Visit [Streamlit Sharing](https://streamlit.io/sharing) for more information.

**Note:** you cannot deploy a streamlit app where the source is a repository owned by the organization, unless you can log into that organization's github account.
This is true even if you have full read/write access to the organization's repositories.
Instead you must create a fork of the repository you want to deploy, and point streamlit.io to that fork.
