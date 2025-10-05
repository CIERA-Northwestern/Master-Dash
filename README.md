# CIERA MASTER Dashboard
This dashboard provides a way for interested individuals to explore data regarding four key CIERA metrics:
1. Press
2. Events
3. Outreach
4. Visits

Instructions are provided below for various levels of usage.
Even if you have never edited code before, the goal of the instructions in [Level 2](#level-2-using-the-dashboard-on-your-computer) is for you to run the dashboard on your computer.
On the other end of things, if you are comfortable with routine use of git, code testing, etc., then jump to [Level 4](#level-4-significant-customization-and-editing) to get an overview of how the dashboard works and what you might want to edit.
To update the dashboard, jump to Level 1: Updating the Configuration and Data](#level-1-updating-the-configuration-and-data).

## Table of Contents

- [Level 0: Using the Dashboard Online](#level-0-using-the-dashboard-online)
- [Level 1: Updating the Configuration and Data](#level-1-updating-the-configuration-and-data)
- [Level 2: Using the Dashboard on your Computer](#level-2-using-the-dashboard-on-your-computer)
- [Level 3: Making Some Edits to the Code](#level-3-making-some-edits-to-the-code)
- [Level 4: Significant Customization and Editing](#level-4-significant-customization-and-editing)
- [Level 5: Additional Features](#level-5-additional-features)

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

There are two ways to update data on the dashboard. If you want to view it quickly and easily, you may select the 'manual upload' option in the dashboard initial prompt, drag-and-dropping the desired data into the upload space. This will display the appropriate dashboard automatically (no need to specify which metric you want to see; if all is formatted correctly, it should be determined from column names), but in a non-persistent format - you will need to reupload the csv every time you want to view it this way.
Alternatively, you may use persistent upload by selecting the other option in initial prompt. Selecting the desired metric will display latest saved csv with appropriate interpretation. to update this go to the raw data folder [here](https://github.com/CIERA-Northwestern/Master-Dash/tree/main/data/raw_data), and add your new csv by clicking on the "Add file" button in the upper right hand corner.
If you update it in this way, please make sure to move the prior version of the data into the 'archived data folder' [here](https://github.com/CIERA-Northwestern/Master-Dash/tree/main/data/archived_data)

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

## Level 5: Additional Features

### Using and Editing Multiple Dashboards

It is recommended that your repositories that use this dashboard template are a fork of the template.
Unfortunately you cannot have multiple official forks of a single repository, nor can you have a private fork, which is necessary for dashboards with sensitive data.
However, you can create a "manual" fork in both cases, as described below.

1. **Create a New Repository**: In your GitHub/Atlassian account, create a new repository. The repository can be set to "Private" if you wish.

2. **Clone the Original Repository**: Clone the public repository to your local machine and navigate to the cloned repository directory.

   ```bash
   git clone https://github.com/zhafen/root-dash.git
   cd your-public-repo
   ```

3. **Change the setup for the remote repositories**: Designate the repository you cloned from as `upstream`, and create a new origin with the url of your private repository.

   ```bash
   git remote rename origin upstream
   git remote add origin https://github.com/<your-username>/<your-private-repo>.git
   ```

4. **Check the result**: If done correctly, the output of `git remote -v` should be

    ```bash
    git remote -v
    ```

    > ```
    > origin  git@github.com:<your-username>.git (fetch)
    > origin  git@github.com:<your-username>.git (push)
    > upstream        git@github.com:zhafen/root-dash.git (fetch)
    > upstream        git@github.com:zhafen/root-dash.git (push)
    > ```

4. **Push to the Private Repository**: Push all branches and tags to your new private repository:

   ```bash
   git push origin --all
   git push origin --tags
   ```

### Continuous Integration

Continuous integration (automated testing) is an excellent way to check if your dashboard is likely to function for other users.
You can enable continuous integration [via GitHub Actions](https://docs.github.com/en/actions/automating-builds-and-tests/about-continuous-integration) (also available in a tab at the top of your github repo), including adding a badge showing the status of your tests
(shown at the top of this page).
Some tests don't work on continuous integration,
and are disabled until the underlying issues are addressed.
Continuous integration can be tested locally using [act](https://github.com/nektos/act),
which may be helpful if the issues that occur during continuous integration are system specific.

### Deploying a Private App
Streamlit has the option to deploy your code without sharing it publicly.
More information can be found [in this section of the Streamlit Sharing documentation](https://docs.streamlit.io/streamlit-community-cloud/share-your-app#make-your-app-public-or-private).


---

ChatGPT was used in the construction of this document.

