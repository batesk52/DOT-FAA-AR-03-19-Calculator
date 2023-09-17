# -*- coding: utf-8 -*-
"""
:::::::::::::::::::NOTEPAD:::::::::::::::::::

 


"""

"""
__________________________________________
_______________      Imports 
__________________________________________

"""
import pandas as pd
import sqlite3
import os
import glob
from tkinter import filedialog as fd
from datetime import datetime

"""
__________________________________________
_______________      SQl Query Library 
__________________________________________

"""

# Datatypes in SQLite3
# NULL
# INTEGER
# REAL
# TEXT
# BLOB

query_tables = """SELECT name FROM sqlite_master  
  WHERE type='table';"""

"""
______________________________________________________________________________
________________                  Methods                    _________________
______________________________________________________________________________



__________________________________________
_______________      Create / Save / Call databases storing raw test data
__________________________________________

"""

def save_rawdata_db(data_raw):
    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    timestamp = datetime.timestamp(dt)
    connection=sqlite3.connect(os.path.join(os.getcwd(),"Database","RawData",
                                            f"{timestamp}.db"))
    cursor=connection.cursor()
    print("connection to database made:")
    for specimen in data_raw.keys():
            cursor.execute(f"CREATE TABLE {specimen} (column1 REAL)")
            print(f"{specimen} created")
            data_raw[specimen].to_sql(f"{specimen}", connection, if_exists="replace")
            print(f"{specimen} entered into database")
            connection.commit()
    connection.close()

def update_rawdata_db(data_raw):
    
    filetypes = (
        ('Database Files', '*.db'),
        ('Excel macro files', '*.xlsxm'))
    file = fd.askopenfilename(
        title='Select Database File',
        initialdir=os.path.join(os.getcwd(),"Database"),
        filetypes=filetypes)
    
    connection=sqlite3.connect(f"{file}")
    cursor=connection.cursor()
    print("connection to database made:")
    
    for specimen in data_raw.keys():
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {specimen}") # drop existing table 
            cursor.execute(f"CREATE TABLE {specimen} (column1 REAL)")
            print(f"{specimen} created")
            data_raw[specimen].to_sql(f"{specimen}", connection, if_exists="replace")
            print(f"{specimen} entered into database")
            connection.commit()
        except:
            print(f"{specimen} failed")
    connection.close()

def load_rawdata_db():
    
    data_all={} #creating nested dictionaries to store data:
    sql_query = """SELECT name FROM sqlite_master  
      WHERE type='table';"""
    
    filetypes = (
        ('Database Files', '*.db'),
        ('Excel macro files', '*.xlsxm'))
    file = fd.askopenfilename(
        title='Select File',
        initialdir=os.path.join(os.getcwd(),"Database"),
        filetypes=filetypes)

    connection=sqlite3.connect(f"{file}")
    cursor=connection.cursor()
    cursor.execute(sql_query)
    specimens = cursor.fetchall()
        
    for specimen in specimens:
        specimen = specimen[0] # need this to convert from tuple to string
        data_all[specimen] = pd.read_sql_query(f'SELECT * from {specimen}', connection,).iloc[:,1:]
        print(f"{specimen} done")
    connection.close()
    return data_all 


# use this to obtain the specific data that you want
def get_from_rawdata(larger_dataset,list_of_specimens):
    data_of_interest={}
    for specimen in list_of_specimens:
        data_of_interest[specimen] = larger_dataset[specimen]
    return data_of_interest


"""
__________________________________________
___________    Create / load databases, derived from Excel Summary sheets
__________________________________________

"""  


def save_results_db():

    # select folder for database to be updated
    folder = fd.askdirectory(initialdir=os.path.join(os.getcwd(),"Input Data"),title = "Select New Data")
    # select folder to save all of the database files
    save_folder = fd.askdirectory(initialdir=os.path.join(os.getcwd(),"Database"),title = "Select Location to Save New Databases")
    
    data_all={} #create dictionary for later use
    data_sub={} #nested dictionary
    
    # Read every excel file in "Input Data"
    materials_dir = glob.glob(rf"{folder}/*.xlsx")
    
    # Read every .db file in "Database"
    # check if there are files in the selected folder; if so, print failure & pass
    db_check = glob.glob(rf"{save_folder}/*.db")
    if len(db_check) != 0:
        print("ERROR: cannot overwrite existing databases!")
        print("(operation cancelled)")
        return
    
    #obtain material / component name from file directory
    materials=[trim.split("\\")[-1][:-5] for trim in materials_dir]
    
    i=0
    mat_property={}
    for material in materials:
        f=pd.ExcelFile(materials_dir[i])
        mat_property[material]=f.sheet_names
        mat_property[material].remove("template")
        mat_property[material].remove("Summary")
        for prop in mat_property[material]:
            # read each sheet in the workbook
            data_sub[prop]=pd.read_excel(materials_dir[i],sheet_name=prop,skiprows=6,
                                     keep_default_na=False)
            # data_sub[prop].drop("Link to Report",axis=1,inplace=True) # if wanted, will remove link
        data_all[material]=data_sub
        data_sub={} #empty dataframe for rewritting later
        i+=1
    
    for material in materials:
        connection=sqlite3.connect(rf"{save_folder}/{material}.db")
        cursor=connection.cursor()
        print(f"connection to {material} database made:")
        for prop in mat_property[material]:
            
            try:
                cursor.execute(f"CREATE TABLE {prop} (column1 REAL)")
                data_all[material][prop].to_sql(f"{prop}", connection, if_exists="replace")
                print(f"{prop} table for {material} made")
                connection.commit()
            except:
                print("ERROR - does a material property sheet have a space?")
                print("Operation Cancelled")
        connection.close()

def load_results_db():    
    data_all, data_sub={},{} #creating nested dictionaries to store data:
    sql_query = """SELECT name FROM sqlite_master  
      WHERE type='table';"""
    
    folder = fd.askdirectory(initialdir=os.path.join(os.getcwd(),"Database"),title = "Select Database folder")
    materials_dir = glob.glob(rf"{folder}/*.db")
    for material in materials_dir:
    
        connection=sqlite3.connect(rf"{material}")
        cursor=connection.cursor()
        cursor.execute(sql_query)
        properties = cursor.fetchall()
        
        for prop in properties:
            prop = prop[0] # need this to convert from tuple to string
            data_sub[prop] = pd.read_sql_query(f'SELECT * from {prop}', connection,).iloc[:,1:]
            print(f"{prop} done")
        data_all[material.split("\\")[-1][:-3]]=data_sub
        print(f"{material} done")
        data_sub = {} # reset child dictionary
    return data_all