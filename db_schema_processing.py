#import pandas as pd
#from sqlalchemy import create_engine
import sys
import json
import pyodbc
from util import calculate_hash, verify_hash, zip_data
import sm_api


from io import StringIO
import gzip

#from  sm_api import get_surveyschema_by_name



# from sqlalchemy.types import Integer
# from  sqlalchemy.schema import Table
# from sqlalchemy import MetaData

#engine = create_engine('mssql+pyodbc://DIRECTIONS\\Aftab.Jalal/ANSA')
#engine = create_engine('sqlite://', echo=False)
conn_str = (
    r'DRIVER={SQL Server};'
    #r'SERVER=DACT-55LT\SQLEXPRESS;'
    r'SERVER=(local)\SQLEXPRESS;'
    r'DATABASE=ANSA;'
    r'Trusted_Connection=yes;'
)

def select(sql_string):
  cnxn = pyodbc.connect(conn_str)
  result = None
  with cnxn:
    cursor = cnxn.cursor()
    cursor.execute(sql_string)
    for row in cursor.fetchall():
      print ("hash from DB : " + row)
      result = row
  return result


def insert(sql_string, *args):
   # Create a cursor from the connection
   cnxn = pyodbc.connect(conn_str)
   with cnxn:
    cursor = cnxn.cursor()
    #jsonstring = "[{'Your Directions / Pathways Details:': {'Your Contact': ['Eurobodalla', 'Vic May']}}, {'Name': ['AFtab', 'Jalal']}, {'*Client Type': 'Own Alcohol and/or Drug Use'}, {'* Principal Substance of Concern ': {'Main Substance of Concern': ['Non-prescribed opioids (eg. heroin)', 'Other']}}, {'SERVICE GOALS What are your goals regarding alcohol / drug use? ': ['Not really wanting to change my use at all']}, {'RISK ASSESSMENTS': {'Any indication of suicidal ideation or history?': 'No', 'Any indication of domestic / family violence?': 'Yes - risk assessment required'}}]"
    #json = a = json.dumps(jsonstring, sort_keys=True)
    cursor.execute(sql_string, *args)
    cnxn.commit()


def get_hash_from_db(survey_name):
    sql = f"select top 1 hash from SurveySchemaJSON where survey_name='{survey_name}'"
    result = select(sql)
    return result

def isok_hash(survey_name, json_string):
  db_hash = get_hash_from_db(survey_name)
  if not db_hash:
    return False
  return verify_hash(json_string, db_hash)
    

def save_schema_json(survey_name, survey_id, json_gzbytes, hsh):
  sql = None
  sql = "insert into SurveySchemaJSON (hash, survey_name, survey_id, survey_schema) values (?, ?, ?,  CAST(? as nVarChar(MAX)))"
  insert( sql, [hsh, survey_name, survey_id, json_gzbytes ])    


def exe():
  survey_name ='MJ ANSA Client Registration'
  schema_json = sm_api.get_surveyschema_by_name(survey_name)
  if 'error' in schema_json:
    print(schema_json)
    sys.exit()

  #print(schema_json)
  print("\n\n------------------------\n")
  survey_id = schema_json['id']

  hash_str = f"{survey_id}_{schema_json['date_modified']}"
  #schema_json_string = json.dumps(schema_json, sort_keys=True)

  if not isok_hash(survey_name, hash_str):
    hsh = calculate_hash(hash_str)
    print(" new hash "  + hsh)
    #schema_file = "json/client_registration_schema.json"
    schema_file = "json/everyday_living.json"
    with open(schema_file, "r") as file:
      schema_json = json.load(file)
      #schema_json_string = json.dumps(schema_json, sort_keys=True)
      compressed = zip_data(schema_json)
      print (len(compressed))
      #print(compressed)
      save_schema_json(survey_name, schema_json['id'], compressed, hsh)
      


  #js = json.dumps(schema_json, sort_keys=True)
  # if new_schema:
  #   save_schema_json(survey_name, survey_id,  new_schema)




if __name__ == '__main__':
  exe()








# with cnxn:
#   # Create a cursor from the connection
#   cursor = cnxn.cursor()

#   jsonstring = "[{'Your Directions / Pathways Details:': {'Your Contact': ['Eurobodalla', 'Vic May']}}, {'Name': ['AFtab', 'Jalal']}, {'*Client Type': 'Own Alcohol and/or Drug Use'}, {'* Principal Substance of Concern ': {'Main Substance of Concern': ['Non-prescribed opioids (eg. heroin)', 'Other']}}, {'SERVICE GOALS What are your goals regarding alcohol / drug use? ': ['Not really wanting to change my use at all']}, {'RISK ASSESSMENTS': {'Any indication of suicidal ideation or history?': 'No', 'Any indication of domestic / family violence?': 'Yes - risk assessment required'}}]"

#   json = a = json.dumps(jsonstring, sort_keys=True)
#   cursor.execute("insert into SurveySubmissionsJSON(slk, survey_type, json_content, has_done_assessment) values (?, ?, ?, ?)", 'FTALL21071981' , 1, json, 0)
#   cnxn.commit()


# df = pd.DataFrame({'name' : ['User 1', 'User 2', 'User 3'] , 'age': ["15", "20", "34"] })

# df.to_sql('users', con=cnxn, dtype={"age": Integer()})

# df
# #engine.execute("SELECT * FROM integers").fetchall()

# users  = Table('users', MetaData(), autoload=True, autoload_with=engine)
# # users 
# # Table('users', MetaData(bind=None), Column('index', BIGINT(), table=<users>), Column('name', TEXT(), table=<users>), Column('age', INTEGER(), table=<users>), schema=None)


 #"#/pages/[page]/questions/[question]"
#  question=""
#  "#/answertype_matrix/rows"
#  "#/answertype_matrix/columns/choices"