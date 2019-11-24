
surveys = {
  "client_registration" : {

    "field_table" : {
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
      'SERVICE GOALS What are your goals regarding alcohol/drug use?': 'Goals'
    },
    "values_table" : {
      'Reduce the harmfulness of my use' : 'ReduceHarmfulness',
      'Not really wanting to change my use at all': 'NotWantChange',
      "Manage the impact of other's alcohol/drug use": 'ManageImpactOthers'    
    },
    "bit_fields" : ['risk_dv' ,'risk_suicide'],
    "skip_fields" : [ 'Contact Information', 'EmergencyContact']
  }
}