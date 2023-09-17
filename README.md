[Project Overview](#overview)

[Steps to Get Started](#steps-to-get-started)

[Documentation](#documentation)


# Overview:

This software project is intended to simplify the process of performing statistical analysis per [DOT/FAA/AR-03/19 - Material Qualification and Equivalency for Polymer Matrix Composite Material Systems (Updated Procedure)](https://www.tc.faa.gov/its/worldpac/techrpt/ar03-19.pdf). There are numerous statistical methods used in this report. One calculation of particular use to me is A & B Basis. [NASA application](https://ntrs.nasa.gov/citations/20040111395) / [FAA application](https://www.mmpds.org/wp-content/uploads/2015/03/mmpds_2015_2007aeromat_presentation.pdf).

In general, A & B Basis allowables can be thought of as additional "factors of safety" that are related to material or compenent variability. These values are calculated using confidence intervals. If the datasets can be:

1) assumed to have a normal population distribution
2) assumed to have equal variance between datasets

then, calculations then become very straightforward: see [Section 5.3 STATISTICAL ANALYSIS](https://www.tc.faa.gov/its/worldpac/techrpt/ar03-19.pdf) for more information on the statistical methods employed.

This tool performs A & B basis calculations assuming that Conditions 1 & 2 are true. In future versions of this tool, additional statistical methods from AR-03/19 will be implemented. A weibull analysis method will be implemented (for cases in which the data is not normally distributed).


# Steps to Get Started

1) Navigate to "Input Data / Project1 / V1.0"
2) Open any of the Excel spreadsheets: each file is a single material, and each sheet is a single material property
3) Familiarize yourself with the structure of the input data. For this analysis, the only columns that MUST be populated are:
   	a) specimen ID
   	b) Value (SI) - this is the value of the material property that is being tracked (in SI units)
   	c) Condition - this is the test environment (RTD, ETD, CTD, etc)
   	d) Method - this is the type of test being run (sometimes, multiple tests are used for the same property & you want to compare them)
5) Run gui.py
6) The user interface should pop up (assuming you've installed the correct libraries).
7)  Select the button, "Update Summary Databases"
8)  A navigation window will open - select the folder containing the version of test data you want to upload to a new database. Then, a new file navigation window will open, asking you where you want to save the data. I recommend you save the data in a new folder, other than V1.0.
9)  If everything works well, the message "New Databases Generated" in the console
10)  Return to the GUI; press "Calculate Material Allowables (A,B Basis).
11)  A navigation pane will open; select the folder containing the database files you want to analyze. This will generate an Excel workbook in the "Exports" folder.
12)  If everything goes well, a message "a-b-basis.xlsx generated in 'Exports' folder" will generate in the console.
13)  Navigate to the "Exports" folder to find the A & B basis calculator


# Documentation

	database.py
	Using this file, raw data that has been entered into excel templates found in "Input Data" can be imported into SQL databases. This can also be used to store raw data as a single SQL database file. It can also update databases with new information.
	• [no class]
		 save_rawdata_db(data_raw)
			Given a dictionary with specimen ID's as keys and raw data as values, this method will create a SQL database which stores the specimen ID as a table, the columns as values, and the individual measurements as entries
			 Arguments:
				 data_raw
					 Dictionary with specimen ID's as the keys, and the raw data of each test as the value
			 Returns:
				 Nothing - a database is created with the time as the filename.
		 update_rawdata_db(data_raw)
			If you have an existing database and want to add / overwrite existing data, use this method. It opens a file explorer & ask to select the database to update.
			 Arguments:
				 data_raw
					 Dictionary with specimen ID's as the keys, and the raw data of each test as the value. This is data that will be appended to, or overwrite existing data in the SQL database
			 Returns:
				 Nothing - the selected database is updated
		 load_rawdata_db()
			Instead of having to import & clean raw data every time you wish to perform analysis, it can be saved in a SQL database to be easier (see save_rawdata_db()). This method imports the data from the selected database. 
			 Arguments:
				 None - run the method, and it will open a file explorer & ask you to navigate to the correct database.
			 Returns:
				 data_all
					 Dictionary with specimen ID's as the keys, and the raw data of each test as the value.
		 get_from_rawdata(larger_dataset,list_of_specimens)
			Given a list of sample names, you can run this code to make a smaller dataset with only the raw data you wish to analyze
			 Arguments:
				 larger_dataset
					 Dictionary with specimen ID's as the keys, and the raw data of each test as the value.
				 list_of_specimens
					 An array of strings, containing sample ID's
			 Returns:
				 data_of_interest
					 Dictionary with specimen ID's as the keys, and the raw data of each test as the value. It is a smaller dataset, containing only the keys that are passed as a list in the list_of_specimens argument
		 save_results_db()
			Use this method to save the excel spreadsheets of choice as SQL databases. Upon running the method, the user is asked to navigate to the folder containing spreadsheets, called "Input Data". Each spreadsheet should be a component, and each sheet page should contain a material property. The method will ignore spreadsheet pages named "template" and "Summary". The summary can be used to take notes & make quick calculations. In order to run correctly, the data must be stored
			 Arguments:
				 None - the user is asked to navigate to the folder containing excel spreadsheets that are to be updated
			 Returns:
				 None - the user is asked where to save the databases of interest. The databases are saved in that folder. 
		 load_results_db()
			In order to run analysis on the summaries collected in excel templates, the user must first import them
			 Arguments:
				 None - the user is asked to navigate to the folder containing SQL databases
			 Returns:
				 data_all
					 Creates a nested dictionary, which is organized as follows:
						 Material
							 Material property
								 Dataframe with results & other datatypes entered

	analyze.py
	Given data in a consistent format, use this file for analysis of test data. It can perform several types of statistical analysis & reports them in a consistent format so they can be used interchangeably with getdata.py, database.by, and report.py
	• Stats(object):
		This class is designed to perform statistical analysis for generating material allowables (hence the name). It is intended to work with the "Input Data" databases.
		○ basis_approx(results,basis)
			calculates the a-basis &-basis values for the given data
			 Arguments:
				 results
					 Dataframes with sample ID's as the index, and data values as column entries
				 Basis
					 either "a" (a-basis) or "b" (b-basis)
			 Returns:
				 basis_val
					 Float value of a or b basis calculation
		○ compare_means(data_a,data_b)
			Compares the means of (2) samples of data. A Shapiro Wilks test is run to check for normality on both datasets. A Levine test is run to check for equal variances between the datasets. If the datasets do not have equal variance, a Welch test is performed. If they do have the same variance, a 2-sample Student T test is run.
			 Arguments:
				 data_a, data_b
					 Dataframes with sample ID's as the index, and data values as column entries
			 Returns:
				  results_df
					 Dataframe containing the analysis
	• Allowables(object):
		This class is designed to perform statistical analysis for generating material allowables (hence the name). It is intended to work with the "Input Data" databases.
		○ summary(data)
			This is an in-progress function that is not fully functional - it is intended to create a summary analysis that is reflective of AGATE / DOT-FAA-AAR documentation
			§ Arguments:
				 data
					 Creates a nested dictionary, which is organized as follows:
						 Material
							 Material property
								 Dataframe with results & other datatypes entered
			§ Returns:
				 data_all
					 a nested dictionary, which is organized as follows:
						 Material
							 Material property
								 Dataframe with results
									 Mean, max, min, std dev, sample size
		○ a_b_basis(data)
			This is an in-progress function that is not fully functional - it is intended to create a summary analysis that is reflective of AGATE / DOT-FAA-AAR documentation
			§ Arguments:
				 data
					 Creates a nested dictionary, which is organized as follows:
						 Material
							 Material property
								 Dataframe with results & other datatypes entered
			§ Returns:
				 data_all
					 a nested dictionary, which is organized as follows:
						 Material
							 Material property
								 Dataframe with results
									 Mean, max, min CoV, A Basis, B Basis, sample size
		○ DOT_FAA_AR_03_019(data):
			TBD
			§ Arguments:
				 TBD
			§ Returns:
				 TBD
		
	• Plot()
		I am still trying to figure out what this does - it seems that it allows you to pass a figure & axis to the following method. If one is not supplied, it will create a 10x8 plot
		○ __init__()
			Creates a figure & axis, if one is not provided
			§ Arguments:
				 none
			§ Returns:
				 none
	• Line_plot()
		I am still trying to figure out what this does - it seems to be a child class to Plot, and it specifies that you pass x & y axes names. 
		○ __init__()
			Creates a figure & axis, if one is not provided
			§ Arguments:
				 none
			§ Returns:
				 none
		○ add_test(test, **kwargs)
			When you pass a dataframe into this method, it will create a line plot using the a & y axes names given in the method.
			§ Arguments:
				 test
					 A dataframe with specimen data as columns & entries as rows
			§ Returns:
				 None - it adds the data of interest to an existing plot
		○ add_tests(test, **kwargs)
			When data is given as a dictionary of raw data, use this method to add all the data to the plot at once.
			§ Arguments:
				 tests
					 Dictionary of raw data, with specimen ID's as keys & test data as values
			§ Returns:
				 None - it adds the data of interest to an existing plot
