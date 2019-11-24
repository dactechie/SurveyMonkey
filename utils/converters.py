from .string_manip import clean, kclean
from .slk import generate_slk
from .qna_mappings import surveys

survey_type = "client_registration"
survey_dict = surveys.get(survey_type)

field_table = survey_dict["field_table"]
values_table = survey_dict["values_table"]
bit_fields = survey_dict["bit_fields"]
skip_fields = survey_dict["skip_fields"]


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


def get_storage_kv_list_AFTER_IMPLEMENTING_TESTSUITE(arb_list: list) -> list:
  result_items = [ get_storage_kv_dict(item) 
                     if isinstance(item, dict)
                     else values_table.get(item, item)
                     for item in arb_list ]
  return [x for x in result_items if x is not None]             



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

def storage_convertor(arb_list):
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

  del results['Name'], results['dob'], results['gender']

  return results
    

def get_text_by_idlist(idlist, dict_array):
  return (clean(dict['text']) for dict in dict_array if dict['id'] in idlist)

def get_idname_dict(container, items_type, name_field='text'):
  return {item['id']: clean(item[name_field]) for item in container[items_type]}