import json
#import sys
from survey_monkey import process_pages
from util import table_storage_convertor, flatten_pages, merge_dicts, getSLK


def exe(schema_file, response_file):
  qna_id_defs = None

  with open(schema_file, "r") as file:
      qna_id_defs = json.load(file)

  with open(response_file, "r") as file:
      answers_json = json.load(file)

  pages = answers_json['pages']

  
  pages.insert(0,[{'response_id' : answers_json['id'], 'survey_id' : answers_json['survey_id']}])
  
  
  res = process_pages(qna_id_defs, pages)
  #print(res)

  # res = flatten_pages(res)
  # res = merge_dicts(results)
  res = table_storage_convertor(res)

  return res
  



if __name__ == '__main__':

  #schema_file = "itsp_optimizm_matrix.json"
  #response_file ="itsp_optimism_response.json"

# 248700530
#  schema_file = "json/itsp_survey_schema.json"
#  response_file="json/itsp_response.json"

  #schema_file = "json/demographic_schema.json"
  #response_file="json/demographic_responses.json"

  #response_file ="json/client_regis_response_manual.json"
  schema_file = "json/client_registration_schema.json"
  response_file="json/client_registration_response.json"
  
  fortables = exe(schema_file, response_file)
  print(fortables)