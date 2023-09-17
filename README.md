
Wherever you want to link to your Real Cool Heading section, put your desired text in brackets, followed by the anchor link in parentheses:
[Go to Real Cool Heading section](#real-cool-heading)


gui.py
	I'm not exactly sure how I want this to look yet. I'm using ChatGPT to expedite
	• [no class]
		○ Function
			TBD
			 Arguments:
				 TBD
			 Returns:
				 TBD

getdata.py
	This file is focussed on collecting, trimming, and storing test data collected from test machines. It also performs basic calculations & exports data into consistent dataframes that calculate some result, which can be 
	• [no class]
		 Initialize()
			Creates the folders: "Input Data", "Database", "References"]
	• RawData(object)
		This class is used to import test data, and import it into a dictionary with specimen ID's as the keys, and test data stored as a dataframe
		 select_file()
			Uses tkinter to open windows explorer & navigate to a file
			 Arguments:
				 None
			 Returns:
				 filename
					 Directory for file
		 select_folder()
			Uses tkinter to open windows explorer & navigate to a folder
			 Arguments:
				 None
			 Returns:
				 filename
					 Directory for folder
		 get_names(ext, folder)
			Finds the names of all files with the given extension in the given directory
			 Arguments:
				 ext
					 The extension of the file of interest ("csv", "dat", etc.)
				 folder
					 Directory to folder containing test data
			 Returns:
				 test_path
					 Array of strings of filepaths to raw data files
				 testname
					 Array of names of each test
		 import_rawdata(ext, software)
			This method will ask that you supply the extension & software as arguments. Then, it will run the clean_rawdata method based on the parameters selected as arguments in this method
			 Arguments:
				 ext
					 The extension of the file of interest ("csv", "dat", etc.)
				 software
					 # indicates what columns need to be renamed, rows to skip when importing data ("TW,"MPT","BH")
			 Returns:
				 data
					 Dictionary with specimen ID's as the keys, and the raw data of each test as the value
		 clean_rawdata(test_path,software)
			This method reads csv files, and applies the necessary edits (renaming columns, skipping rows, etc.) to import raw test data from multiple file types. 
			 Arguments:
				 test_path
					 String containing the directory to the file that is to be imported
				 software
					 String input to identify which software package generated the raw data files being imported ("MPT", "BH", "NT", etc.)
			 Returns:
				 data
					 Dictionary with specimen ID's as the keys, and the raw data of each test as the value
		 change_sign(data,metric)
			If you want to change the sign of imported data in a selected column, use this method
			 Arguments:
				 data
					 A dataframe with raw data from a single test
					 Or
					 A dictionary with sample ID's as keys and raw data as a dataframe as dictionary values
				 metric
					 String containing the name of the column which is to be sign-changed
			 Returns:
				 data
					 Changes the sign of the selected column in-place; does not create a new variable
	• Summary(object)
		Using this class, perform quick calculations on data that has been imported directly from raw test files. Frequently, this data is copy/pasted into the Excel Spreadsheet needed. It will create a dataframe with specimen ID's as the index, and specimen results as the column entries
		 all_max_values(data)
			returns the maximum value from every available column in the list.
			 Arguments:
				 data
					 collection of raw data in dictionary
			 Returns:
				 data_all
					 Dataframe with all maxes calculated

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

#Real Cool Heading

report.py
	This file is designed for creating automated PDF reports 
	• PDF()
		This class contains all the templates for PDF reporting. Child classes can use the templates generated in this class.
		○ Function
			TBD
			§ Arguments:
				□ TBD
		○ Function 2
			TBD
			§ Arguments:
				□ TBD
	• AGATE_WP3_3_033051_115(PDF)
		This is a child method of the PDF class. The PDF class houses the templates, and the Report class creates different configurations of these pages. As the name suggests, this class is used to recreate AGATE WP3.3-033051-115
		○ Function
			TBD
			§ Arguments:
				□ TBD
		○ Function 2
			TBD
			§ Arguments:
				□ TBD

BRL_study.py
	Loads all raw data from BRL database
	• [no class]
		 convert_units(rawdata)
			 Used to convert lbf to kN, in to mm, Farenheit to Celsius
			 Arguments:
				 Rawdata
					 Data data from test machine, imported into standard format
			 Returns:
				 rawdata
					 Modifies the argument & returns it in converted units
		 brl(dataframe_dict, od_inches)
			 Used to calculate BRL in kilo-pounds per linear inch, from test data stored as kilonewtons & millimeters
			 Arguments:
				 dataframe_dict
					 Dataframe with specimen ID's as the keys, and the raw data of each test as the value
				 od_inches
					 The outer diameter of the tube tested, in inches
			 Returns:
				 TBD
