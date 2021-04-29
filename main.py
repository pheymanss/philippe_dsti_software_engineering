# reviews that needed packages are present
#if not, automatically attempt an installation
import package_install as pkg
pkg.precheck_imports(['os','pyodbc','pandas'])

# import packages
import pyodbc
import os
import pandas as pd

# import modules
import dynamic_sql
import trigger_functions as tg
import secure_db_connect as sdbc

welcome = """
Data ScienceTech Institute
---------------------------------------
Project Submission 
Software Engineering + Data Wrangling 
---------------------------------------
Developed by Philippe Heymans Smith
philippe.heymans-smith@dsti.institute.edu

Version 1.0
2021-04-22"""

print(welcome)

# encrypt as soon as user inputs the password
# this means the password is never explicitly in a variable 
run_pw = sdbc.obfuscate(input("Please enter the SQL server password: "))

print('Connecting to database...')
conn = sdbc.connect(driver='SQL Server',
                    server='FILIP',
                    database='Survey_Sample_A18',
                    user='tester',
                    enc_password=run_pw)

print('Reviewing SurveyStructure...')
trigger, new_survey_struct = tg.should_run_procedure(conn)


if (trigger):
    print('Updating database view according to new version of SurveyStructure...')
    update_query = dynamic_sql.update_survey_view(new_survey_struct)
    conn.cursor().execute(update_query)
    
    print('Extracting newly refreshed view...')
    pd.read_sql('SELECT * FROM vw_AllSurveyData', conn).to_csv('vw_AllSurveyData.csv',
                                                               index=False)
    print("""Process finished. The refreshed versions of 'SurveyStructure.csv' and 'vw_AllSurveyData.csv'
are now in the present working directory.""")
else:
    print("Process finished.")