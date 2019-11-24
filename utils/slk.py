
from .string_manip import cleanse_string


def generate_slk(name, dob, sex):
  firstname, lastname = name
  '''
  DOB string in US format
  '''
  dob = f"{dob[3]}{dob[4]}/{dob[0]}{dob[1]}/{dob[-4:]}"
  
  return getSLK(firstname, lastname, dob, sex)


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