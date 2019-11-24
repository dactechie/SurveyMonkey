#import sys
#import re

from utils.string_manip import clean, kclean #, get_text_by_idlist, get_idname_dict
from utils.converters import storage_convertor,  get_text_by_idlist, get_idname_dict
from sm_matrix_utils import handle_col_choices, handle_nocols, handle_otherids
# id_types = ['row_id', 'col_id', 'choice_id']
# id_types_list_map = {'row_id':'rows' , 'col_id': 'cols', 'choice_id': 'choices'}

# meta data to store 
'''
"href": "https://api.surveymonkey.net/v3/surveys/271026860/responses/11075389573",
 "date_created": "2019-10-18T00:34:54+00:00", 
 "date_modified": "2019-10-18T11:22:40+00:00", "response_status": "completed", 
 "collector_id": "247867892", 
'''

'''
  survey_schema : json object
'''
def extract_response(survey_schema, answers_json):
  pages = answers_json['pages']
  
  # TODO insert datetime of the submission
  pages.insert(0,[{'response_id' : answers_json['id'], 'survey_id' : answers_json['survey_id']}])
  
  res = process_pages(survey_schema, pages)
  res = storage_convertor(res)

  return res
  

def process_question(schema_question, question):
  question_text = clean(schema_question['headings'][0]['heading'])
  results = None
  txt_replace_fn = qtype_handlers.get(schema_question['family'])
  if txt_replace_fn:
    results = {question_text : txt_replace_fn(schema_question, question)}
    #print (results)
  else:
    print(f"\n\n...........family : {schema_question['family']}\n\n")
  
  return results



def schema_for_question_id(schema_questions, response_qid):
  return next(sq for sq in schema_questions if sq['id'] == response_qid)


def process_page(sch_qs, response_qs):

  q_schemas__respq = [(schema_for_question_id(sch_qs, resp_q['id']), resp_q) 
                        for resp_q in response_qs]

  # some questions may not have been answered, filter them out
  q_schemas__respq = filter(lambda qs: qs[0] != None, q_schemas__respq)

  return [process_question(q_schema, resp_q)
            for q_schema, resp_q in q_schemas__respq]
 
    

def process_pages(qna_id_defs, pages):

  results = [pages.pop(0)] # meta information like date_Created, survey_id , response_id 

  for counter, page in enumerate(pages):
    res = process_page(qna_id_defs['pages'][counter]['questions'],
                       page['questions'])
    results.append(res)

  return results


# def process_pages(qna_id_defs, pages):
#   results = []
#   meta = pages.pop(0)
#   for counter, page in enumerate(pages):
#     res = process_page(qna_id_defs['pages'][counter], page)
#     results.append(res)
#   results.insert(0, meta)
#   return results

    #return [process_page(qna_id_defs['pages'][counter], page)  for counter, page in enumerate(pages) ]


def get_text_qna_open_ended(schema_question, data):
  if len(data['answers']) == 1:
    return clean(data['answers'][0]['text'])

  return  [clean(answer['text']) for answer in data['answers'] ]


def get_text_qna_single_choice(schema_question, data):
  chosens = get_text_qna_mcq(schema_question, data)
  return chosens[0]
 

def get_text_qna_mcq(schema_question, data):
  sch_anss = schema_question['answers']  
  chosens = []
  ans_ch_ids = [answer.get('choice_id') for answer in data['answers']]
  if ans_ch_ids:
    chosens = list(get_text_by_idlist(ans_ch_ids, sch_anss['choices']))

  if sch_anss.get('other'):
    anstext = [clean(answer['text']) for answer in data['answers'] if 'other_id' in answer]
    if anstext:
      chosens.append(anstext[0])

  return chosens

#def get_idname_dict(container, items_type, name_field='text'):
#  return {item['id']: clean(item[name_field]) for item in container[items_type]}
#

def process_demographics(schema, data):

  rows  =  get_idname_dict(schema['answers'], 'rows', 'type')
  results = [ {rows[dans['row_id']]: dans['text']} for dans in data['answers'] ]

  return results


def build_text_matrix_with_cols (schema):

  rows = get_idname_dict(schema, 'rows')
  cols = get_idname_dict(schema, 'cols')
  
  cols_choices = { col['id']: get_idname_dict(col, 'choices')
                   for col in schema['cols']  }
  return rows, cols, cols_choices



def process_matrix_with_cols_AFTERIMPLEMENTING_TESTSUITE(matrix_schema, data):
  rows, cols, cols_choices = build_text_matrix_with_cols (matrix_schema['answers'])
  
  results1, data_answers = handle_otherids(data['answers']) #data_answers now has no other_ids
  results2, data_answers = handle_nocols(data_answers, rows, cols, cols_choices ) # data
  results3 = handle_col_choices(data_answers)
  return {**results1, **results2, **results3}
      


def process_matrix_with_cols(matrix_schema, data):
  rows, cols, cols_choices = build_text_matrix_with_cols (matrix_schema['answers'])
  results =  {} #{'rows': rows.values(), 'cols': cols.values()}

  for answer in data['answers']:
    row_id = answer.get('row_id')
    if not row_id and answer.get('other_id'):
      results['other'] = answer['text']
      continue
    
    rtext = rows[row_id]
    ans_col_id = answer['col_id']
    ans_choice_id = answer['choice_id']

    ctext = cols[ ans_col_id ]
    col_choices = cols_choices[ ans_col_id ]
    if not ctext:
      results[rtext] = clean(col_choices[ans_choice_id])  # not a list unlike below ..append and = []
      continue

    ans = clean(col_choices[ans_choice_id]) 
    # { clean(ctext) : clean(col_choices[ans_choice_id]) }
    
    if results.get(rtext):
      results[rtext].append(ans)
    else:
      results[rtext]= [ans]
       
  rr = {}
  for k, v in results.items():
      if len(v) == 1:
        rr[k] = v[0]
      else:
        rr[k] = v
        
  return rr


def build_text_matrix_no_cols (schema): # answers schema
  rows = { row['id']: clean(row['text']) 
           for row in schema['rows'] }

  choices = { choice['id']: clean(choice['text']) 
              for choice in schema['choices'] }
  return rows, choices


def process_matrix_with_NO_cols_AFTERIMPLEMENTING_TESTSUITE(matrix_schema, data):
  rows, choices = build_text_matrix_no_cols (matrix_schema['answers'])
  
  results1, data_answers = handle_otherids(data['answers']) #data_answers now has no other_ids

  ...



def process_matrix_no_cols(matrix_schema, data):
  rows, choices = build_text_matrix_no_cols (matrix_schema['answers'])
  results = []
  for answer in data['answers']:
    #{'other_id': '2413710781', 'text': 'sexting'}
    row_id = answer.get('row_id')
    if not row_id and answer.get('other_id'):
      results.append({'other' : answer['text']})
      continue

    rtext = rows[answer['row_id']]
    ans_choice_id = answer['choice_id']
    if not rtext:
      results.append(choices [ans_choice_id])
    else:
      results.append ({rtext : choices [ans_choice_id]})
      #print("SHOULD NOT COME  HERE : process_matrix_no_cols")
      #sys.exit()

  return results


def get_text_qna_matrix(matrix_schema, data):
  if matrix_schema['id'] != data['id']:

    print("Error - question IDs don't match. \n\t")
    return None

  if matrix_schema['answers'].get('cols'):
    return process_matrix_with_cols (matrix_schema, data)
  else:
    return process_matrix_no_cols (matrix_schema, data)


qtype_handlers = {
  'matrix' : get_text_qna_matrix,
  'multiple_choice' : get_text_qna_mcq,
  'single_choice': get_text_qna_single_choice,
  'open_ended': get_text_qna_open_ended,
  'datetime' : get_text_qna_open_ended,
  'demographic' : process_demographics
}

'''

def process_demographics(schema, data):
  rows  =  get_idname_dict(schema['answers'], 'rows', 'type')
  results = []
  
  for answer in data['answers']:
    row_id = answer.get('row_id')
    rtext = rows[row_id]
    results.append ({rtext : answer ['text']})

process page
  # for resp_q in response_qs:
  #   q_schema = schema_for_question_id(sch_qs, resp_q['id'])
  #   if not q_schema: # seome qustions may be skipped
  #     continue
  #   res = process_question(q_schema, resp_q)
  #   results.append(res)
  # return results
'''


'''
def get_text_qna_mcq(schema_question, data):  
  #chosens  = []
...
  # if other_id:
  #   other_id = other_id['id']
  
  # for answer in data['answers']:
  #   chosen_id = answer['choice_id']
  #   chosen = get_text_by_id(chosen_id, schema_question['answers']['choices'])
  #   if chosen:
  #     chosens.append(chosen)
  #   elif other_id and chosen_id == other_id:
  #     chosens.append(clean(schema_question['answers']['other']['text']))
    
  return chosens



# def process_matrix_with_cols(matrix_schema, data):
#   rows, cols, cols_choices = build_text_matrix_with_cols (matrix_schema['answers'])

#   results = {  clean(rows[answer['row_id']]) : [] for answer in data['answers'] }
  
#   for answer, row_label in data['answers'] :
#     ans_col_id = answer['col_id']
#     ans_choice_id = answer['choice_id']
    
#     ctext = cols[ ans_col_id ]
#     col_choices = cols_choices[ ans_col_id ]
#     if not ctext:
#       results[row_label] = clean(col_choices[ans_choice_id])
#       continue

#     results[row_label].append({ clean(ctext) : clean(col_choices[ans_choice_id]) })

#   return results
    

  '''