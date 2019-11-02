import random
import json
from datetime import datetime, timezone
from util import random_date

#SKIP random rows
SKIP_ROW_PERCENT = 0.7

today = datetime.now()

todaystr = today.strftime("%m/%d/%Y %H:%M %p")
d1 = datetime.strptime('1/1/1958 1:30 PM', '%d/%m/%Y %I:%M %p')
d2 = datetime.strptime('1/1/2005 4:50 AM', '%d/%m/%Y %I:%M %p')

#for i in range(1,10):
bdaystr =   random_date(d1, d2).strftime("%m/%d/%Y")
#print(f"{bdaystr}")

#sys.exit()


def rand(min=0, max=10):
  return random.randint(min, max)


def family_matrix(data):
  answers = [ ]
  #can_skip = False
  # if len(data['rows']) > 3:
  #   can_skip = True

  if 'cols' in data:
    for c in data['cols']:      
      # if can_skip and random.random() > SKIP_ROW_PERCENT:
      #   continue                # skip random rows
      num_choices = len(c['choices'])
      for r in data['rows']:
        answers.append ({ 'row_id': r['id'],
                          'col_id': c['id'],
                          'choice_id': c['choices'][rand(0, num_choices-1)]['id']
                        })
  else: # rating
    num_choices = len(data['choices'])
    for r in data['rows']:
      # if can_skip and random.random() > SKIP_ROW_PERCENT:
      #   continue                # skip random rows
      answers.append ({ 'row_id': r['id'],
                        'choice_id': data['choices'][rand(0, num_choices-1)]['id']
                      })
  #print(json.dumps(answers,indent=2))
  return answers


def family_single_choice(data):

  answers = data['answers']
  # Current Substances of Concern and Method of use <br>Has any of this changed in the last 4 weeks?"
  if data['id'] == "359675782":  
    return {'choice_id': answers['choices'][0]['id']}  # Yes

  num_choices = len(answers['choices'])
  return {'choice_id': answers['choices'][rand(0, num_choices-1)]['id']}


def family_open_ended(data):
  heading = data['headings'][0]['heading']
 # print(f"\n\t\t  open ended {heading} \n ")

  validation = data.get('validation', False)
  result = 0
  if validation and validation['type'] == 'integer': #some single_choice / slider
    result = str(rand(int(validation['min']), int(validation['max'])))
  else:
    result = 'open ended answer for ' + heading

# {'heading': 'Client Reference'}  # 'id':'238283939'
  return {'text': result}

# https://github.com/SurveyMonkey/public_api_docs/blob/master/includes/_responses.md
##Open Ended Multi/Numerical, Demographic, Datetime
#        "answers": [{
#            "row_id": "12345678",
#            "text": "Sample Text Response" ##(format depends on question type, "12/31/2015 11:59 PM" for datetime)
#        }]


def family_datetime(data):
  
  row_id = data['answers']['rows'][0]['id']
  heading = data['headings'][0]['heading']
  result = {'row_id' : row_id} 
  
  if str.lower(heading) =='date of birth':
    result['text'] = bdaystr  #'20/05/1981'
    return result

  result['text'] = todaystr #'10/10/2019' # 12/31/2015 11:59 PM
  return result


#file = './registration.json'
#file = './date_test.json'
#file = './itsp_survey_schema.json'
#file = './initial_assesment.json'
file = './json/client_registration_schema.json'
#file = './json/mj_rego_schema.json'

data ={} 

with open (file, 'r') as f:
  data = json.load(f)

#print(data)
utc_str = str(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+10:00"))
postData = {'ip_address': "127.0.0.1",  "date_created": utc_str}
pages = []

for p in data['pages']:
  page = {'id' : p['id']}
  questions = []

  for q in p['questions']:
    question = { 'id' : q['id']}

    if q['family'] == 'matrix':
      #if 'cols' in q['answers']:
      question['answers'] = family_matrix(q['answers'])

    elif q['family'] == 'single_choice' or q['family'] == 'multiple_choice':
      rand_answer = family_single_choice(q)
      question['answers'] = [rand_answer]
    elif q['family'] == 'open_ended':
      rand_answer = family_open_ended(q)
      question['answers'] = [rand_answer]
    elif q['family'] =='datetime':
      rand_answer = family_datetime(q)
      question['answers'] = [rand_answer]
    elif q['family'] =='demographic':
      continue
    else:
      #print(q)
      question['answers'] = ['\nTo be implemented> ' + q['family'] +'\n']
    
    questions.append(question)

  page['questions'] = questions
  pages.append(page)


postData['pages'] = pages

print(json.dumps(postData, indent=2))
