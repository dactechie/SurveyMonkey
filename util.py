import re
from random import randrange
from datetime import timedelta


#re.compile("[^A-Za-zs?.0-9()]")
patHTML = re.compile('<[^<]+?>')
patParen = re.compile(r'\([^)]*\)')  # note: mutates the answers


alpha_pattern = re.compile(r'[\W_0-9]+')
cleanse_string = lambda string: alpha_pattern.sub('', string)

#no_unicode_pattern = re.compile(r'[^\x00-\x7F]+')
#remove_unicode = lambda string: no_unicode_pattern.sub('', string)


def get_23(name):    
    return name.ljust(3, '2')[1:3]


def get_235(name):
    five = name.ljust(5, '2')
    return f"{five[1:3]}{five[4]}"



def getSLK(firstname, lastname, DOB_str, sex_str):
    """
    Expects DOB_str to be in "ddmmyyyy" or "dd/mm/yyyy" format
    sex_str must be 'Male' or 'Female' , everything else is converted to 9
    """
    last = get_235(cleanse_string(lastname))
    first = get_23(cleanse_string(firstname))
    
    name_part = (last + first).upper()
    
    if sex_str == 'Male':
        sex_str = '1'
    elif sex_str == 'Female':
        sex_str = '2'
    else:
        sex_str = '9'   # TODO    'if not unknown, add a Warning ?'
    
    return name_part + DOB_str.replace("/","") + sex_str

bit_fields = [
 'risk_dv' ,'risk_suicide'
]

skip_fields = [
  'Contact Information', 'EmergencyContact'
]
# skip_exception [
#   {'Contact Information': 'zip'}
# ]

field_table = {
  'Your Contact' : 'Team.Staff',
  'Your Nominated Emergency Contact':'EmergencyContact',
  #'Country of Birth': 'COB',
  'Date of birth':'dob',
  'Indigenous Status': 'atsi',
  'Client Type': 'client_type',
  #'Preferred Language': ''
  'Gender Identity': 'gender',
  'How were you referred to Pathways/Directions?': 'ReferralSource',
  'Main Substance of Concern' :'PDC',
  'Other substance of concern 1': 'ODC1',
  'Other substance of concern 2': 'ODC2',
  'Other substance of concern 3': 'ODC3',
  'Other substance of concern 4': 'ODC4',
  'Other substance of concern 5': 'ODC5',
  'Any other addictive behaviours that concern you?': 'OtherAddictiveBehaviour',
  'Any indication of suicidal ideation or history?': 'risk_suicide',
  'Any indication of domestic/family violence?': 'risk_dv',
  'Do you have any immediate concerns for the safety and wellbeing of either yourself or others?': 'safety_concern',
  'Are you experiencing any current thoughts of death/dying or hurting yourself?': 'thoughts_selfharm',
  "Discussion about Directions' services Initial support identified": 'ServicesIdentified',
  'SERVICE GOALS What are your goals regarding alcohol/drug use?': 'Goals',
  
}


values_table = {
  'Reduce the harmfulness of my use' : 'ReduceHarmfulness',
  'Not really wanting to change my use at all': 'NotWantChange',
  "Manage the impact of other's alcohol/drug use": 'ManageImpactOthers',
  
}


import string
printable = set(string.printable)

'''
  not to be used when storing the JSON verbatim
'''
def kclean(string):
  key = patParen.sub('', string).strip()
  return key

def clean(string):
  unicode = patHTML.sub(' ', string).replace('  ', ' ').strip('*^: ')
  unicode = unicode.replace(' / ','/')  # MDS Data Collection  - no spaces around /:  'Not stated/inadequately',99)
  return ''.join(filter(lambda x: x in printable, unicode))


def get_storage_kv_dict(arb_dict: dict) -> dict:
  results = {}
  for k, v in arb_dict.items():
    vv = v
    if isinstance(vv, dict):
      r = get_storage_kv_dict(vv)
      results = {**results, **r}
      continue
    elif isinstance(vv, list):
      vv = get_storage_kv_list(vv)
    else:
      vv = kclean(vv)
    #else:
    #  vv = values_table.get(vv,vv)  - doesnt come here

    field = kclean(k)
    field = field_table.get(field, field)
    if field in skip_fields:
      continue

    if field in bit_fields:      
      results[field] = 0 if vv == 'No' else 1
    else:    
      results[field] = vv

  return results


def get_storage_kv_list(arb_list: list) -> list:
  results = []
  for item in arb_list:
    if isinstance(item, dict):
      r = get_storage_kv_dict(item)
      if r:
        results.append(r)
    # elif isinstance(item, list):
    #   newlist = get_storage_kv_list(item)
    #   results = results + newlist
    else:
      results.append(values_table.get(item, item))

  return results


def flatten_pages(pages):
  flattened_pages = []
  
  for page in pages:
    flattened_pages.extend(page)
    
  return flattened_pages

def merge_dicts(data):
  return {k: v for d in data for k, v in d.items()}


# def flatten_hard_vals(data):
#   hardval_keys = ['client_id', 'safety_concern' , 'thoughts_selfharm', 'risk_suicide', 'risk_dv']
'''
  DOB string in US format
'''
def generate_slk(name, dob, sex):
  firstname, lastname = name
  dob = f"{dob[3]}{dob[4]}/{dob[0]}{dob[1]}/{dob[-4:]}"
  return getSLK(firstname, lastname,dob, sex)


def table_storage_convertor(arb_list):
  results = []
  for item in arb_list:
    if isinstance(item, dict):
      r = get_storage_kv_dict(item)
      if r:
        results.append(r)
    elif isinstance(item, list):
      r = get_storage_kv_list(item)
      results.append(r)

  results = flatten_pages(results)
  results = merge_dicts(results)

  results['team'], results['staff'] = results['Team.Staff']
  del results['Team.Staff']

  results['PDC'], results['method_of_use'] = results['PDC']

  slk = generate_slk(results['Name'], results['dob'], results['gender'])
  results['client_id'] = slk

  del results['Name']

  return results
    

def get_text_by_idlist(idlist, dict_array):
  return (clean(dict['text']) for dict in dict_array if dict['id'] in idlist)

def get_idname_dict(container, items_type, name_field='text'):
  return {item['id']: clean(item[name_field]) for item in container[items_type]}


# def get_choices(col):
#   return {choice['id']: clean(choice['text']) for choice in col['choices']}


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
  