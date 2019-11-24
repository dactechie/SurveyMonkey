import re
import string

#re.compile("[^A-Za-zs?.0-9()]")
patHTML = re.compile('<[^<]+?>')
patParen = re.compile(r'\([^)]*\)')  # note: mutates the answers


alpha_pattern = re.compile(r'[\W_0-9]+')
cleanse_string = lambda string: alpha_pattern.sub('', string)

#no_unicode_pattern = re.compile(r'[^\x00-\x7F]+')
#remove_unicode = lambda string: no_unicode_pattern.sub('', string)



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