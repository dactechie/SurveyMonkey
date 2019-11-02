# from pymongo import MongoClient

# #cluster = MongoClient("mongodb+srv://mj:cool@cluster0-upg7n.mongodb.net/test?retryWrites=true&w=majority")
# cluster = MongoClient("mongodb://localhost:C2y6yDjf5%2FR%2Bob0N8A7Cgv30VRDJIWEHLM%2B4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw%2FJw%3D%3D@localhost:10255/admin?ssl=true")
# db = cluster.get_default_database()

# resp_collection = db.get_collection("ANSAResponses")

# response = {'response_id': '11095161359', 'survey_id': '271875304', 'Country of Birth': 'India', 'Preferred Language': 'English',
#             'atsi': 'Torres Strait Islander but not Aboriginal origin', 'gender': 'Female', 'dob': '07/19/2000', 
#             'client_type': 'Own Alcohol and/or Drug Use', 'ReferralSource': 'Other community/health care service', 
#             'PDC': 'Benzodiazepines - non-prescribed', 'ODC1': 'Cannabis', 'ODC2': 'Alcohol', 'other': 'none', 
#             'Goals': ['ReduceHarmfulness', 'NotWantChange', 'ManageImpactOthers'], 
#             'ServicesIdentified': ['Group participation', 'Althea GP', 'Althea Nurse', 'Althea Psychologist'],
#             'safety_concern': 'malicious shaming', 'thoughts_selfharm': 'yes', 'risk_suicide': 1, 'risk_dv': 1, 
#             'CHECKLIST': 'Risk Assessments Completed', 'team': 'Bega Valley', 'staff': 'Tracy Sims', 'method_of_use': 'Inject', 
#             'client_id': 'M22J2190720002'}

# resp_collection.insert_one(response)
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors

# Local development , start the server like this from an admin command lin 
#"C:\Program Files\Azure Cosmos DB Emulator\Microsoft.Azure.Cosmos.Emulator.exe" /EnableMongoDbEndpoint

#import urllib3
#urllib3.disable_warnings()

config = {
    'ENDPOINT': 'https://localhost:8081',
    'PRIMARYKEY': 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==',
    'DATABASE': 'CosmosDatabase',
    #'CONTAINER': 'CosmosContainer'
    'CONTAINER' : 'ANSAResponses'
}

# Initialize the Cosmos client
client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                    'masterKey': config['PRIMARYKEY']})

client.GetDatabaseAccount()
# # Create a database
db = None

try:
    db = client.CreateDatabase({'id': config['DATABASE']})
except errors.HTTPFailure:
    db = client.ReadDatabase("dbs/" + config['DATABASE'])
# db = client.CreateDatabase({'id': config['DATABASE']})

# Create container options
options = {
    'offerThroughput': 400
}

container_definition = {
    'id': config['CONTAINER']
}

# Create a container
try:
  container = client.CreateContainer(db['_self'], container_definition, options)
except errors.HTTPFailure:
  
    db = client.ReadDatabase("dbs/" + config['DATABASE'])



response = {'response_id': '11095161359', 'survey_id': '271875304', 'Country of Birth': 'India', 'Preferred Language': 'English',
            'atsi': 'Torres Strait Islander but not Aboriginal origin', 'gender': 'Female', 'dob': '07/19/2000', 
            'client_type': 'Own Alcohol and/or Drug Use', 'ReferralSource': 'Other community/health care service', 
            'PDC': 'Benzodiazepines - non-prescribed', 'ODC1': 'Cannabis', 'ODC2': 'Alcohol', 'other': 'none', 
            'Goals': ['ReduceHarmfulness', 'NotWantChange', 'ManageImpactOthers'], 
            'ServicesIdentified': ['Group participation', 'Althea GP', 'Althea Nurse', 'Althea Psychologist'],
            'safety_concern': 'malicious shaming', 'thoughts_selfharm': 'yes', 'risk_suicide': 1, 'risk_dv': 1, 
            'CHECKLIST': 'Risk Assessments Completed', 'team': 'Bega Valley', 'staff': 'Tracy Sims', 'method_of_use': 'Inject', 
            'client_id': 'M22J2190720002'}

# Create and add some items to the container
item1 = client.CreateItem(container['_self'], response)

 