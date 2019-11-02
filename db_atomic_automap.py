from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, Integer
from sqlalchemy.ext.automap import automap_base


def _setup_db_reflection_base():

  engine = create_engine(r'mssql+pyodbc://(local)\SQLEXPRESS/ANSA?driver=SQL+Server+Native+Client+11.0') #, echo=True)
  # produce our own MetaData object
  metadata = MetaData()
  # we can reflect it ourselves from a database, using options  such as 'only' to limit what tables we look at...
  metadata.reflect(engine, only=['ClientRegistration'])# 'lk_gender'])
  
  #metadata.create_all

  # we can then produce a set of mappings from this MetaData.
  Base = automap_base(metadata=metadata)
  Base.prepare() # calling prepare() just sets up mapped classes and relationships.
 
  session = Session(engine)
  
  return Base, session



# data = {'Team.Staff': ['Bega Valley', 'Tracy Sims'], 'Country of Birth': 'India', 'Preferred Language': 'English', 
# 'atsi': 'Torres Strait Islander but not Aboriginal origin', 'Name': ['MJ', 'JM'], 'Sex': 'Female', 'dob': '07/19/2000', 
# 'client_type': 'Own Alcohol and/or Drug Use', 'ReferralSource': 'Other community/health care service', 
# 'PDC': ['Benzodiazepines - non-prescribed', 'Inject'], 'ODC1': 'Cannabis', 'ODC2': 'Alcohol', 'other': 'none', 
# 'Goals': ['ReduceHarmfulness', 'NotWantChange', 'ManageImpactOthers'], 'ServicesIdentified': ['Group participation', 
# 'Althea GP', 'Althea Nurse', 'Althea Psychologist'], 'safety_concern': 'malicious shaming', 'thoughts_selfharm': 'yes', 
# 'risk_suicide': 1, 'risk_dv': 1, 'CHECKLIST': 'Risk Assessments Completed'}
# {'dob': '07/19/2000'}, 
data_lkups = [  {'gender': 'Female'} ]
# data_hard =  {'response_id': '11095161359', 'survey_id': '271875304','client_id': 'with respose id', 'team': 1, 'staff': 1,
# 'safety_concern': 'None' , 'thoughts_selfharm': 'always troubling ' , 'risk_suicide': 1, 'risk_dv': 0, 'dob': '07/01/2000'}

data_hard =  {'client_id': 'with respose id','response_id': '11095161359', 'survey_id': '271875304',
'safety_concern': 'None' , 'thoughts_selfharm': 'always troubling ' , 'risk_suicide': 1, 'risk_dv': 0, 'dob': '07/01/2000'}

# dat = {'response_id': '11095161359', 'survey_id': '271875304', 'Team.Staff': ['Bega Valley', 'Tracy Sims'], 'Country of Birth': 'India', 
# 'Preferred Language': 'English', 'atsi': 'Torres Strait Islander but not Aboriginal origin', 'Name': ['MJ', 'JM'], 'Sex': 'Female', 
# 'dob': '07/19/2000', 'client_type': 'Own Alcohol and/or Drug Use', 
# 'ReferralSource': 'Other community/health care service', 'PDC': ['Benzodiazepines - non-prescribed', 'Inject'],
#  'ODC1': 'Cannabis', 'ODC2': 'Alcohol', 'other': 'none', 'Goals': ['ReduceHarmfulness', 'NotWantChange', 'ManageImpactOthers'],
#   'ServicesIdentified': ['Group participation', 'Althea GP', 'Althea Nurse', 'Althea Psychologist'], 'safety_concern': 'malicious shaming', 
#   'thoughts_selfharm': 'yes', 'risk_suicide': 1, 'risk_dv': 1, 'CHECKLIST': 'Risk Assessments Completed'}

def insert(data_ids=data_lkups, raw=data_hard):
  Base, session = _setup_db_reflection_base()
  
  # mapped classes are ready
  #ClientRegistration, LkGender = Base.classes.ClientRegistration, Base.classes.lk_gender  
  ClientRegistration = Base.classes.ClientRegistration
  #genderObj = session.query(LkGender).filter(LkGender.name==data_ids['gender']).first()
  
  client = ClientRegistration(gender=1, staff=1, team=8, **raw)

  session.add(client)
  session.commit()


if __name__ =='__main__':
  insert()


# u1 = session.query(ClientRegTemp).first()

# print(u1.id)

# aa = session.query(LkGender).filter(LkGender.id==2).first()
# print(aa.name)
## print(LkGender)