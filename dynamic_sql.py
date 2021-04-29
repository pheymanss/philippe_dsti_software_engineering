def question_subquery(survey_id, question_id):
    """Builds the subquery for a QuestionId, mapped to its corresponding SurveyId.

    Args:
        survey_id (str/int): The number of the SurveyId. Will be casted to string. 
        question_id ([str]): The number of the QuestionId. Will be casted to string. 
    """
    try:
        question_id = str(question_id)
        survey_id = str(survey_id)
    except: Exception    
        
    query = f""" 
    COALESCE(
	(SELECT A.Answer_Value
	 FROM Survey_Sample_A18.dbo.Answer as A
         WHERE A.SurveyId = {survey_id}  
    	 AND A.QuestionId = {question_id}
    	 AND A.UserId = U.UserId),
         -1) AS Q{question_id},"""
    return query


def survey_subquery(survey_id, question_ids):
    """Builds the subquery for a list QuestionId's, mapped to its corresponding 
    (single) SurveyId.

    Args:
        survey_id (str/int): The number of the SurveyId. Will be casted to string. 
        question_id ([str]): List of QuestionId's. Will be casted to string.
    """
    questions = ''
    
    for qs in question_ids:
        questions = questions + question_subquery(survey_id, qs)
    
    query = f"""
        SELECT 
        U.UserId,
        {str(survey_id)} as SurveyId,
        {questions[:-1]}
        FROM
    	Survey_Sample_A18.dbo.[User] as U 
        WHERE EXISTS
        (
        	SELECT *
        	FROM
        		Survey_Sample_A18.dbo.Answer as A
        	WHERE U.UserId = A.UserId
        	AND A.SurveyId = {str(survey_id)})"""
    return query

def update_survey_view(new_survey_struct):
    """Build the query to update the view 'vw_AllSurveyData', which has the 
    following structure:
    
    UserId | SurveyId | Q1 | Q2 | ... | QN
    --------------------------------------
     XXXXX |        1 |  2 |  5 | ... |  8
     XXXXX |        3 | -1 |  1 | ... |  8
     XXXXX |        1 |  2 |  2 | ... |  8
     XXXXX |        1 |  7 |  2 | ... |  8
     XXXXX |        2 |  2 |  1 | ... |  8
    
    The layout of the rows and columns are dictated by the specification of 
    [Survey_Sample_A18].[dbo].[SurveStructure], which indicates the indexes of 
    each question contained in each survey. To keep the column consistency 
    across all different surveys, missing questions from a survey will be
    imputed as '-1'.
 
    Args:
        new_survey_struct (pd): A pandas DataFrame with a snapshot of 
        Survey_Sample_A18.dbo.SurveStructure.
    """
    question_ids = new_survey_struct['QuestionId'].unique()
    
    survs = """
    
UNION
    
""".join([survey_subquery(surv_id, question_ids) for surv_id in new_survey_struct['QuestionId'].unique()])


    query = 'CREATE OR ALTER VIEW vw_AllSurveyData AS ' + survs + ';'
    return query
