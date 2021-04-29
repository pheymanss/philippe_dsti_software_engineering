import package_install as pkg
pkg.precheck_imports(['os', 'pandas']) 

import pandas as pd
import os

def should_run_procedure(con):
    """ 
    Determines whether or not the trigger condition for the stored procedure 
    is met (ie the structure of SurveyStructure has changed since the previous run.)

    Args:
        con: A SQL connection to the database
    """
    
    # fetch the latest version of the survey structure
    new_struct = pd.read_sql("SELECT * FROM dbo.SurveyStructure", con)
    
    # compare this new snapshot against the previous one (in case a previous one exists)
    if os.path.exists('SurveyStructure.csv'):
        return compare_structs(con), new_struct
    else:
        new_struct.to_csv('SurveyStructure.csv', index=False)
        print('No previous snapshot of SurveyStructure was found. A refresh of the view will be executed.')
        return True, new_struct


def compare_structs(con):
    """Compares the structure of the new snapshot of SurveyStructure against the new one 

    Args:
        con: A SQL connection to the database
    """
    
    # This function performs an outer merge to review the two snapshots
    # of SurveyStruct. 
     
    # query a new version of the snapshot directly from the SQL server
    new_snap = pd.read_sql("SELECT * FROM dbo.SurveyStructure", con)
    
    # read the last snapshot taken, currently stored locally in a .csv file
    current_snap = pd.read_csv('SurveyStructure.csv')
    
    # add flags to each snapshot
    current_snap['current_snap'] = ['current'] * len(current_snap.index)
    new_snap['new_snap'] = ['new'] * len(new_snap.index)
    
    # if any row has a NaN value on either the new or current flag columns,
    # then the structure must have changed.
    mrg = pd.merge(left=current_snap, right=new_snap, how='outer')
    
    run_trigger = mrg.isna().values.any()
    
    if run_trigger:
        # update the current SurveyStructure stored locally
        new_snap.to_csv('SurveyStructure.csv', 
                        index=False, 
                        columns=['SurveyId','QuestionId','OrdinalValue'])
        print('Found a change in the specifications of SurveyStructure. A refresh of the view will be executed.')
    else:
        print('The structure of the survey has not changed. No refresh of the view is needed.')
    return run_trigger

