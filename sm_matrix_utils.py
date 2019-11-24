
from utils.string_manip import clean

def handle_otherids(data_answers):
  results = {}
  otherid_indices = [ index-1 
                      for index, answer in enumerate(data_answers) 
                      if not answer.get('row_id') and answer.get('other_id')]
  if otherid_indices:
    if len(otherid_indices) > 1:
      print ("more than one other_id. Not handled, skipping......")
    else:
      answer = list.pop(data_answers, otherid_indices[0])
      results['other'] = answer['text']

  return results, data_answers


'''
 a matrix question can have zero or more columns

  One or more columns :
      Then each column would have a list of choices
      cols_choices is a list of choices for all the columns for the question.
      (process_matrix_with_cols )
      The answer to each of the cells in such a matrix question i.e. the answer to the sub-question, 
      depends on teh following:
      if there is a list of 'column HEADERS' cols["23423col-id"], 
          the answer pertains to the column text of each particular column (in the context of the row sub-question)
      otherwise (no columns HEADERS):
          the answer pertains to just the row text. schema-rowtext['answer-row-id'] i.e. rtext_dict
      
  if there are no columns  e.g. Team ,  staff question...
      if not row_id and answer.get('other_id'):
        results.append({'other' : answer['text']})
        continue
      
      rtext = rows[answer['row_id']]
      ans_choice_id = answer['choice_id']
      if not rtext:
        results.append(choices [ans_choice_id])
      else:
        results.append ({rtext : choices [ans_choice_id]})

'''

ids_tuple = lambda answer, cols_choices:  ( answer.get('row_id') ,  (cols_choices[answer['col_id']] , answer['choice_id']))

def get_ids_coltext(data_answers, cols, cols_choices, with_col_text: False):
  if with_col_text:
    return  ( ( index-1 , ids_tuple(answer, cols_choices) )
              for index, answer in enumerate(data_answers) if not cols[answer['col_id'] ]
            )
  else:
    return  ( ( index-1 , ids_tuple(answer, cols_choices) )
              for index, answer in enumerate(data_answers) if cols[answer['col_id'] ]
            )


def handle_nocols(data_answers, rtext_dict, cols, cols_choices):
  results = {}
  
  ids = get_ids_coltext (data_answers, cols, cols_choices, with_col_text=False)

  for idx in ids:
    data_answers.pop(idx[0])
  # data answerrs now only has stuff WITH cols

  for idx in ids:
    rid, col_choices_chid  = idx[1]

    col_choices, choice_id = col_choices_chid
    rtext = rtext_dict[rid]    
     
    results [rtext] = clean(col_choices[choice_id]) 

  return results, data_answers # popped out answers with no cols



def handle_col_choices(data_answers):
  results = {}
  ids = get_ids_coltext (data_answers, cols, cols_choices, with_col_text=True)

  return results, data_answers
