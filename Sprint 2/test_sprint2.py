import unittest
import sprint2
import mock
from prettytable import PrettyTable

def test_legal_marriage(age):
    family_dic = {
        '@F1@': {'FAM': '@F1@',
                'HUSB_NAME': 'Ned /Stark/',
                'HUSB': '@I8@',
                'WIFE_NAME': 'Kate /Stark/',
                'WIFE': '@I3@',
                'FAM_CHILD': ['@I9@'],
                'CHIL': '@I9@',
                'MARR': '2000-3-24',
                'DIV': 'NA',
                'husband_object': {'INDI': '@I8@',
                                    'NAME': 'Ned /Stark/',
                                    'SEX': 'M',
                                    'BIRT': f'{age}-3-17',
                                    'INDI_CHILD': 'NA',
                                    'SPOUSE': ['@F1@'],
                                    'DEAT': 'NA',
                                    'ALIVE': True},
                'wife_object': {'INDI': '@I3@',
                                'NAME': 'Kate /Stark/',
                                'SEX': 'F',
                                'BIRT': '1980-7-10',
                                'INDI_CHILD': ['@F5@'],
                                'SPOUSE': ['@F1@'],
                                'DEAT': 'NA',
                                'ALIVE': True}
            }
    }
    
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []
    sprint2.is_marriage_legal()

    return len(sprint2.anomaly_array) == 0

def test_over_age_150():
    individuals={
        '@I1@': {'INDI': '@I1@',
                'NAME': 'Jimmy /Colon/',
                'SEX': 'M',
                'BIRT': '1860-6-5',
                'INDI_CHILD': ['@F2@'],
                'SPOUSE': ['@F1@'],
                'DEAT': 'NA',
                'AGE': '190',
                'ALIVE': True},
        '@I2@': {'INDI': '@I2@',
                'NAME': 'Helen /Colon/',
                'SEX': 'F',
                'BIRT': '1850-12-10',
                'DEAT': '2009-6-2',
                'INDI_CHILD': 'NA',
                'SPOUSE': ['@F1@'],
                'AGE': '159',
                'ALIVE': False}}
                    
    sprint2.individuals = individuals
    sprint2.anomaly_array = []
    sprint2.is_age_legal()
    
    return sprint2.anomaly_array==['ANOMALY: INDIVIDUAL: US07: @I1@: More than 150 years old - Birth Date 1860-6-5',
    'ANOMALY: INDIVIDUAL: US07: @I2@: More than 150 years old at death - Birth Date 1850-12-10: Death Date 2009-6-2']

def test_less_age_150():
    individuals={
        '@I1@': {'INDI': '@I1@',
                'NAME': 'Jimmy /Colon/',
                'SEX': 'M',
                'BIRT': '1960-6-5',
                'INDI_CHILD': ['@F2@'],
                'SPOUSE': ['@F1@'],
                'DEAT': 'NA',
                'AGE': '49',
                'ALIVE': True},
        '@I2@': {'INDI': '@I2@',
                'NAME': 'Helen /Colon/',
                'SEX': 'F',
                'BIRT': '1950-12-10',
                'DEAT': '2009-6-2',
                'INDI_CHILD': 'NA',
                'SPOUSE': ['@F1@'],
                'AGE': '59',
                'ALIVE': False}}
                    
    sprint2.individuals = individuals
    sprint2.anomaly_array = []
    sprint2.is_age_legal()
    
    return len(sprint2.anomaly_array) == 0


def test_dates_pass(date,ddate,bdate,fdate):
    
    family_dic={'@F8@': {'FAM': '@F8@',
  'HUSB_NAME': 'George /Nickson/',
  'HUSB': '@I18@',
  'WIFE_NAME': 'Kitty /Nilson/',
  'WIFE': '@I13@',
  'FAM_CHILD': ['@I19@'],
  'CHIL': '@I19@',
  'MARR': f'{date}',
  'DIV': f'{ddate}'}}
    
    
    individuals={'@I1@': {'INDI': '@I1@',
  'NAME': 'Jimmy /Colon/',
  'SEX': 'M',
  'BIRT': f'{bdate}',
  'INDI_CHILD': ['@F2@'],
  'SPOUSE': ['@F1@'],
  'DEAT': 'NA',
  'AGE': '9',
  'ALIVE': True},
 '@I2@': {'INDI': '@I2@',
  'NAME': 'Helen /Colon/',
  'SEX': 'F',
  'BIRT': f'{fdate}',
  'DEAT': 'NA',
  'INDI_CHILD': 'NA',
  'SPOUSE': ['@F1@'],
  'AGE': '13',
  'ALIVE': False}}
    
    sprint2.family_dic = family_dic
    sprint2.individuals=individuals
    sprint2.anomaly_array = []
    sprint2.validate_dates()

    return len(sprint2.anomaly_array)==0


def test_dates_error(date,ddate,bdate,fdate):
    
    family_dic={'@F8@': {'FAM': '@F8@',
  'HUSB_NAME': 'George /Nickson/',
  'HUSB': '@I18@',
  'WIFE_NAME': 'Kitty /Nilson/',
  'WIFE': '@I13@',
  'FAM_CHILD': ['@I19@'],
  'CHIL': '@I19@',
  'MARR': f'{date}',
  'DIV': f'{ddate}'}}
    
    
    individuals={'@I1@': {'INDI': '@I1@',
  'NAME': 'Jimmy /Colon/',
  'SEX': 'M',
  'BIRT': f'{bdate}',
  'INDI_CHILD': ['@F2@'],
  'SPOUSE': ['@F1@'],
  'DEAT': 'NA',
  'AGE': '9',
  'ALIVE': True},
 '@I2@': {'INDI': '@I2@',
  'NAME': 'Helen /Colon/',
  'SEX': 'F',
  'BIRT': f'{fdate}',
  'DEAT': 'NA',
  'INDI_CHILD': 'NA',
  'SPOUSE': ['@F1@'],
  'AGE': '81',
  'ALIVE': False}}
    
    sprint2.family_dic = family_dic
    sprint2.individuals=individuals
    sprint2.anomaly_array = []
    sprint2.validate_dates()

    return sprint2.anomaly_array==[f'ERROR: FAMILY: US01: @F8@: Family has marrige date {date} later than today',
                                 f'ERROR: FAMILY: US01: @F8@: Family has divorce date {ddate} later than today',
                                 f'ERROR: INDIVIDUAL: US01: @I1@: Individual has birth date {bdate} later than today']

def test_birth_before_marraige_do_nothing():
    family_dic = {'@F1@':{'MARR':'1968-6-4','husband_object':{'INDI':'@I1@','BIRT':'1950-11-8'},'wife_object':{'INDI':'@I2@','BIRT':'1960-11-8'}}}
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []
    
    sprint2.is_birth_before_marraige()
    
    assert len(sprint2.anomaly_array) == 0
    return True


def test_birth_after_marraige_appended_to_error():
    family_dic = {'@F1@':{'MARR':'1968-6-4','husband_object':{'INDI':'@I1@','BIRT':'1970-11-8'},'wife_object':{'INDI':'@I2@','BIRT':'1960-11-8'}}}
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []
    
    sprint2.is_birth_before_marraige()
    
    assert sprint2.anomaly_array[0] == "ERROR: INDIVIDUAL: US02: @I1@: Person has marriage date 1968-6-4 before birth date 1970-11-8"
    return True

# User_Story_29: List all deceased individuals in a GEDCOM file
# Success test 
@mock.patch("sprint2.printTable")
def test_list_deceased_individuals_success(mock_printTable):
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT"]
    current_dic = {'@I6@': {'INDI': '@I6@', 'NAME': 'Stephen /Chang/', 'SEX': 'M', 'BIRT': '1935-12-5', 'DEAT': '2005-4-15', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F2@'], 'AGE': '70', 'ALIVE': False}}
    sprint2.individuals = current_dic
    sprint2.listDeceased()
    mock_printTable.assert_called_with("US29: Deceased People Table", allFields, tagNames, current_dic)
    return True

	
# User_Story_29: List all deceased individuals in a GEDCOM file
# Failed test: Person is dead but has no Death Date
@mock.patch("sprint2.printTable")
def test_list_deceased_individuals_error(mock_printTable):
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT"]
    current_dic = {'@I6@': {'INDI': '@I6@', 'NAME': 'David /Chang/', 'SEX': 'M', 'BIRT': '2002-12-5', 'DEAT': 'NA', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F7@'], 'AGE': '79', 'ALIVE': False}}
    sprint2.individuals = current_dic
    sprint2.listDeceased()
    mock_printTable.assert_called_with("US29: Deceased People Table", allFields, tagNames, {}) #provide empty dictionary so that it won't overwrite
    return True
	
# User_Story_30: List all living married people in a GEDCOM file
# Success test
@mock.patch("sprint2.printTable")
def test_list_living_married_individuals_success(mock_printTable):

    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]
    current_dic = {'@I1@': {'INDI': '@I1@', 'NAME': 'Johnny /Chang/', 'SEX': 'M', 'BIRT': '1958-9-6', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F1@'], 'DEAT': 'NA', 'AGE': '61', 'ALIVE': True}}
    sprint2.individuals = current_dic
    sprint2.listLivingMarried()
    mock_printTable.assert_called_with("US30: Living & Married People Table", allFields, tagNames, current_dic)
    return True

# User_Story_30: List all living married people in a GEDCOM file
# Failed test
@mock.patch("sprint2.printTable")
def test_list_living_married_individuals_error(mock_printTable):
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]
    current_dic = {'@I4@': {'INDI': '@I1@', 'NAME': 'Michael /Chang/', 'SEX': 'M', 'BIRT': '1958-9-6', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F3@'], 'DEAT': '2002-9-6', 'AGE': '61', 'ALIVE': False}}
    sprint2.individuals = current_dic
    sprint2.listLivingMarried()
    mock_printTable.assert_called_with("US30: Living & Married People Table", allFields, tagNames, {}) #provide empty dictionary so that it won't overwrite
    return True


def test_less_than_15_siblings(sib_dic):
    family_dic = sib_dic
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []
    
    sprint2.check_sibling_count()

    return len(sprint2.anomaly_array) == 0

def test_unique_family_name_and_birth_pass():
    family_dic = {'@F1@': {'FAM': '@F1@',
                            'HUSB_NAME': 'Samuel /Venzon/',
                            'HUSB': '@I6@',
                            'WIFE_NAME': 'Willodean /Malagon/',
                            'WIFE': '@I1@',
                            'FAM_CHILD': ['@I7@', '@I13@'],
                            'CHIL': '@I13@',
                            'MARR': '1970-7-7',
                            'DIV': 'NA',
                            'children_objects': [{'INDI': '@I7@',
                                'NAME': 'Beth /Venzon/',
                                'SEX': 'M',
                                'BIRT': '1973-7-8',
                                'INDI_CHILD': ['@F1@'],
                                'SPOUSE': ['@F5@'],
                                'DEAT': 'NA',
                                'AGE': '46',
                                'ALIVE': True},
                                {'INDI': '@I13@',
                                    'NAME': 'Beth /Venzon/',
                                    'SEX': 'F',
                                    'BIRT': '1973-7-8',
                                    'INDI_CHILD': ['@F1@'],
                                    'SPOUSE': 'NA',
                                    'DEAT': 'NA',
                                    'AGE': '44',
                                    'ALIVE': True}]}}
    
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []
    sprint2.unique_family_name_and_birth()

    return sprint2.anomaly_array==['ANOMALY: INDIVIDUAL: US25: @I13@: @I7@: Individuals share the same name Beth /Venzon/ and birth date 1973-7-8 from family @F1@']

def test_unique_family_name_and_birth_error():
    family_dic =  {'children_objects': [{'INDI': '@I30@',
                                        'NAME': 'Chet /Malagon/',
                                        'SEX': 'M',
                                        'BIRT': '1943-8-18',
                                        'INDI_CHILD': ['@F3@'],
                                        'SPOUSE': 'NA',
                                        'DEAT': 'NA',
                                        'AGE': '76',
                                        'ALIVE': True},
                                        {'INDI': '@I31@',
                                            'NAME': 'Sock /Malagon/',
                                            'SEX': 'F',
                                            'BIRT': '1955-10-17',
                                            'INDI_CHILD': ['@F3@'],
                                            'SPOUSE': 'NA',
                                            'DEAT': 'NA',
                                            'AGE': '63',
                                            'ALIVE': True}]}
    
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []
    sprint2.unique_family_name_and_birth()

    return len(sprint2.anomaly_array) == 0


def test_unique_name_and_birth_pass(year):
    individuals = {'@I31@': {'INDI': '@I31@',
                             'NAME': 'Sock /Malagon/',
                             'SEX': 'F',
                             'BIRT': '1955-10-17',
                             'INDI_CHILD': ['@F3@'],
                             'SPOUSE': 'NA',
                             'DEAT': 'NA',
                             'AGE': '63',
                             'ALIVE': True},
                   '@I35@': {'INDI': '@I35@',
                             'NAME': 'Sock /Malagon/',
                             'SEX': 'F',
                             'BIRT': f'{year}-10-17',
                             'INDI_CHILD': ['@F9@'],
                             'SPOUSE': 'NA',
                             'DEAT': 'NA',
                             'AGE': '63',
                             'ALIVE': True}}

    sprint2.individuals = individuals
    sprint2.anomaly_array = []

    sprint2.unique_name_and_birth()

    return sprint2.anomaly_array == [
        'ANOMALY: INDIVIDUAL: US23: @I35@: @I31@: Individuals have the same name Sock /Malagon/ and birth date 1955-10-17']


def test_different_male_last_name():
    family_dic = {'@F1@': {'HUSB_NAME': 'Harry /Potter/', 'FAM_CHILD': ['@I1@', '@I10@'],
                           'children_objects': [{'INDI': '@I1@', 'SEX': 'M', 'NAME': 'Chandler /Bing/'},
                                                {'INDI': '@I10@', 'SEX': 'M', 'NAME': 'Chandler /Potter/'}]}}
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []

    sprint2.check_last_names()
    return sprint2.anomaly_array[
               0] == 'ANOMALY: INDIVIDUAL: US16: @I1@: Individual has different last name Bing than family Potter'


def test_same_male_last_name():
    family_dic = {'@F1@': {'HUSB_NAME': 'Harry /Potter/', 'FAM_CHILD': ['@I1@', '@I10@'],
                           'children_objects': [{'INDI': '@I1@', 'SEX': 'M', 'NAME': 'Joey /Potter/'},
                                                {'INDI': '@I10@', 'SEX': 'M', 'NAME': 'Chandler /Potter/'}]}}
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []

    sprint2.check_last_names()

    return len(sprint2.anomaly_array) == 0

def test_birth_before_marriage_fail():
    """ Test code for US08 (fail) """
    
    family_dic = {'@F1@': {'FAM': '@F1@',
                            'HUSB_NAME': 'Samuel /Venzon/',
                            'HUSB': '@I6@',
                            'WIFE_NAME': 'Willodean /Malagon/',
                            'WIFE': '@I1@',
                            'FAM_CHILD': ['@I7@', '@I13@'],
                            'CHIL': '@I13@',
                            'MARR': '1973-7-7',
                            'DIV': '1980-12-1',
                            'husband_object': {'INDI': '@I6@',
                                                'NAME': 'Samuel /Venzon/',
                                                'SEX': 'M',
                                                'BIRT': '1958-12-6',
                                                'INDI_CHILD': 'NA',
                                                'SPOUSE': ['@F1@'],
                                                'DEAT': 'NA',
                                                'AGE': '60',
                                                'ALIVE': True},
                            'wife_object': {'INDI': '@I1@',
                                            'NAME': 'Willodean /Malagon/',
                                            'SEX': 'F',
                                            'BIRT': '1958-7-7',
                                            'INDI_CHILD': ['@F2@'],
                                            'SPOUSE': ['@F1@'],
                                            'DEAT': 'NA',
                                            'AGE': '61',
                                            'ALIVE': True},
                            'children_objects': [{'INDI': '@I7@',
                                                'NAME': 'Byron /Vezon/',
                                                'SEX': 'M',
                                                'BIRT': '1973-7-6',
                                                'INDI_CHILD': ['@F1@'],
                                                'SPOUSE': ['@F5@'],
                                                'DEAT': 'NA',
                                                'AGE': '46',
                                                'ALIVE': True},
                                                {'INDI': '@I13@',
                                                'NAME': 'Beth /Venzon/',
                                                'SEX': 'F',
                                                'BIRT': '1981-9-8',
                                                'INDI_CHILD': ['@F1@'],
                                                'SPOUSE': 'NA',
                                                'DEAT': 'NA',
                                                'AGE': '44',
                                                'ALIVE': True}]}}
    
    
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []
    sprint2.birth_before_marriage()

    return sprint2.anomaly_array == ['ANOMALY: INDIVIDUAL: US08: @I7@: Child was born at 1973-7-6 before marriage of parents 1973-7-7',
 'ANOMALY: INDIVIDUAL: US08: @I13@: Child was born at 1981-9-8 after 9 month divorce of parents 1980-12-1']

def test_birth_before_marriage_pass():
    """ Test code for US08 (pass) """
    
    family_dic = {'@F1@': {'FAM': '@F1@',
                        'HUSB_NAME': 'Samuel /Venzon/',
                        'HUSB': '@I6@',
                        'WIFE_NAME': 'Willodean /Malagon/',
                        'WIFE': '@I1@',
                        'FAM_CHILD': ['@I7@', '@I13@'],
                        'CHIL': '@I13@',
                        'MARR': '1973-7-7',
                        'DIV': 'NA',
                        'husband_object': {'INDI': '@I6@',
                                            'NAME': 'Samuel /Venzon/',
                                            'SEX': 'M',
                                            'BIRT': '1958-12-6',
                                            'INDI_CHILD': 'NA',
                                            'SPOUSE': ['@F1@'],
                                            'DEAT': 'NA',
                                            'AGE': '60',
                                            'ALIVE': True},
                        'wife_object': {'INDI': '@I1@',
                                        'NAME': 'Willodean /Malagon/',
                                        'SEX': 'F',
                                        'BIRT': '1958-7-7',
                                        'INDI_CHILD': ['@F2@'],
                                        'SPOUSE': ['@F1@'],
                                        'DEAT': 'NA',
                                        'AGE': '61',
                                        'ALIVE': True},
                        'children_objects': [{'INDI': '@I7@',
                                            'NAME': 'Byron /Vezon/',
                                            'SEX': 'M',
                                            'BIRT': '1978-7-6',
                                            'INDI_CHILD': ['@F1@'],
                                            'SPOUSE': ['@F5@'],
                                            'DEAT': 'NA',
                                            'AGE': '46',
                                            'ALIVE': True},
                                            {'INDI': '@I13@',
                                                'NAME': 'Beth /Venzon/',
                                                'SEX': 'F',
                                                'BIRT': '1978-7-8',
                                                'INDI_CHILD': ['@F1@'],
                                                'SPOUSE': 'NA',
                                                'DEAT': 'NA',
                                                'AGE': '44',
                                                'ALIVE': True}]}}
    
    
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []
    sprint2.birth_before_marriage()

    return len(sprint2.anomaly_array) == 0

def test_birth_before_death_fail():
    """ Test code for US09 (fail) """
    
    family_dic = {'@F1@': {'FAM': '@F1@',
                            'HUSB_NAME': 'Samuel /Venzon/',
                            'HUSB': '@I6@',
                            'WIFE_NAME': 'Willodean /Malagon/',
                            'WIFE': '@I1@',
                            'FAM_CHILD': ['@I7@', '@I13@'],
                            'CHIL': '@I13@',
                            'MARR': '1973-7-7',
                            'DIV': 'NA',
                            'husband_object': {'INDI': '@I6@',
                                                'NAME': 'Samuel /Venzon/',
                                                'SEX': 'M',
                                                'BIRT': '1958-12-6',
                                                'INDI_CHILD': 'NA',
                                                'SPOUSE': ['@F1@'],
                                                'DEAT': '1988-10-6',
                                                'AGE': '60',
                                                'ALIVE': True},
                            'wife_object': {'INDI': '@I1@',
                                            'NAME': 'Willodean /Malagon/',
                                            'SEX': 'F',
                                            'BIRT': '1958-7-7',
                                            'INDI_CHILD': ['@F2@'],
                                            'SPOUSE': ['@F1@'],
                                            'DEAT': '1987-12-6',
                                            'AGE': '61',
                                            'ALIVE': True},
                            'children_objects': [{'INDI': '@I7@',
                                                'NAME': 'Byron /Vezon/',
                                                'SEX': 'M',
                                                'BIRT': '1988-1-9',
                                                'INDI_CHILD': ['@F1@'],
                                                'SPOUSE': ['@F5@'],
                                                'DEAT': 'NA',
                                                'AGE': '46',
                                                'ALIVE': True},
                                                {'INDI': '@I13@',
                                                'NAME': 'Beth /Venzon/',
                                                'SEX': 'F',
                                                'BIRT': '1989-7-8',
                                                'INDI_CHILD': ['@F1@'],
                                                'SPOUSE': 'NA',
                                                'DEAT': 'NA',
                                                'AGE': '44',
                                                'ALIVE': True}]}}
    
    
    sprint2.family_dic = family_dic
    sprint2.error_array = []
    sprint2.birth_before_death()

    return sprint2.error_array == ['ERROR: INDIVIDUAL: US09: @I7@: Child was born at 1988-1-9 after death of mother 1987-12-6', 
    'ERROR: INDIVIDUAL: US09: @I13@: Child was born at 1989-7-8 after death of mother 1987-12-6',
    'ERROR: INDIVIDUAL: US09: @I13@: Child was born at 1989-7-8 after 9 month death of father 1988-10-6']

def test_birth_before_death_pass():
    """ Test code for US09 (pass) """
    
    family_dic = {'@F1@': {'FAM': '@F1@',
                            'HUSB_NAME': 'Samuel /Venzon/',
                            'HUSB': '@I6@',
                            'WIFE_NAME': 'Willodean /Malagon/',
                            'WIFE': '@I1@',
                            'FAM_CHILD': ['@I7@', '@I13@'],
                            'CHIL': '@I13@',
                            'MARR': '1973-7-7',
                            'DIV': 'NA',
                            'husband_object': {'INDI': '@I6@',
                                                'NAME': 'Samuel /Venzon/',
                                                'SEX': 'M',
                                                'BIRT': '1958-12-6',
                                                'INDI_CHILD': 'NA',
                                                'SPOUSE': ['@F1@'],
                                                'DEAT': '1988-10-6',
                                                'AGE': '60',
                                                'ALIVE': True},
                            'wife_object': {'INDI': '@I1@',
                                            'NAME': 'Willodean /Malagon/',
                                            'SEX': 'F',
                                            'BIRT': '1958-7-7',
                                            'INDI_CHILD': ['@F2@'],
                                            'SPOUSE': ['@F1@'],
                                            'DEAT': '1987-12-6',
                                            'AGE': '61',
                                            'ALIVE': True},
                            'children_objects': [{'INDI': '@I7@',
                                            'NAME': 'Byron /Vezon/',
                                            'SEX': 'M',
                                            'BIRT': '1980-1-9',
                                            'INDI_CHILD': ['@F1@'],
                                            'SPOUSE': ['@F5@'],
                                            'DEAT': 'NA',
                                            'AGE': '46',
                                            'ALIVE': True},
                                            {'INDI': '@I13@',
                                            'NAME': 'Beth /Venzon/',
                                            'SEX': 'F',
                                            'BIRT': '1980-7-8',
                                            'INDI_CHILD': ['@F1@'],
                                            'SPOUSE': 'NA',
                                            'DEAT': 'NA',
                                            'AGE': '44',
                                            'ALIVE': True}]}}
    
    
    sprint2.family_dic = family_dic
    sprint2.error_array = []
    sprint2.birth_before_death()

    return len(sprint2.error_array) == 0


# US20 Aunts and uncles - success
def aunts_and_uncles_success():
    individuals = {'@I1@': {'INDI': '@I1@', 'INDI_LINE': 14, 'NAME': 'David /Chang/', 'NAME_LINE': 15, 'SEX': 'M', 'SEX_LINE': 19, 'BIRT': '1988-7-9', 'INDI_CHILD': ['@F1@'], 'SPOUSE': 'NA', 'FAMC_LINE': 22, 'DEAT': 'NA', 'BIRT_LINE': 22, 'AGE': '31', 'ALIVE': True}, '@I2@': {'INDI': '@I2@', 'INDI_LINE': 23, 'NAME': 'Johny /Chang/', 'NAME_LINE': 24, 'SEX': 'M', 'SEX_LINE': 28, 'BIRT': '1958-8-9', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F1@'], 'FAMS_LINE': 31, 'DEAT': 'NA', 'BIRT_LINE': 31, 'AGE': '61', 'ALIVE': True}, '@I3@': {'INDI': '@I3@', 'INDI_LINE': 32, 'NAME': 'Nancy /Tsai/', 'NAME_LINE': 33, 'SEX': 'F', 'SEX_LINE': 37, 'BIRT': '1960-9-6', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F1@'], 'FAMS_LINE': 40, 'DEAT': 'NA', 'BIRT_LINE': 40, 'AGE': '59', 'ALIVE': True}}
    family_dic = {'@F1@': {'FAM': '@F1@', 'FAM_LINE': 47, 'HUSB_NAME': 'Johny /Chang/', 'HUSB_LINE': 42, 'HUSB': '@I2@', 'WIFE_NAME': 'Nancy /Tsai/', 'WIFE_LINE': 43, 'WIFE': '@I3@', 'FAM_CHILD': ['@I1@'], 'CHIL_LINE': 44, 'CHIL': '@I1@', 'MARR': '1980-3-2', 'DIV': 'NA', 'husband_object': {'INDI': '@I2@', 'INDI_LINE': 23, 'NAME': 'Johny /Chang/', 'NAME_LINE': 24, 'SEX': 'M', 'SEX_LINE': 28, 'BIRT': '1958-8-9', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F1@'], 'FAMS_LINE': 31, 'DEAT': 'NA', 'BIRT_LINE': 31, 'AGE': '61', 'ALIVE': True}, 'wife_object': {'INDI': '@I3@', 'INDI_LINE': 32, 'NAME': 'Nancy /Tsai/', 'NAME_LINE': 33, 'SEX': 'F', 'SEX_LINE': 37, 'BIRT': '1960-9-6', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F1@'], 'FAMS_LINE': 40, 'DEAT': 'NA', 'BIRT_LINE': 40, 'AGE': '59', 'ALIVE': True}, 'children_objects': [{'INDI': '@I1@', 'INDI_LINE': 14, 'NAME': 'David /Chang/', 'NAME_LINE': 15, 'SEX': 'M', 'SEX_LINE': 19, 'BIRT': '1988-7-9', 'INDI_CHILD': ['@F1@'], 'SPOUSE': 'NA', 'FAMC_LINE': 22, 'DEAT': 'NA', 'BIRT_LINE': 22, 'AGE': '31', 'ALIVE': True}]}}
    
    sprint2.individuals = individuals
    sprint2.family_dic = family_dic
    
    assert sprint2.is_uncle_aunt_marriage_legal() == True
    return True

# US20 Aunts and uncles - error
def aunts_and_uncles_error():
    individuals = {'@I1@': {'INDI': '@I1@', 'INDI_LINE': 14, 'NAME': 'David /Chang/', 'NAME_LINE': 15, 'SEX': 'M', 'SEX_LINE': 19, 'BIRT': '1988-7-9', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F1@'], 'FAMS_LINE': 22, 'FAMC_LINE': 23, 'DEAT': 'NA', 'BIRT_LINE': 23, 'AGE': '31', 'ALIVE': True}, '@I2@': {'INDI': '@I2@', 'INDI_LINE': 24, 'NAME': 'Johny /Chang/', 'NAME_LINE': 25, 'SEX': 'M', 'SEX_LINE': 29, 'BIRT': '1958-8-9', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F2@'], 'FAMS_LINE': 32, 'DEAT': 'NA', 'BIRT_LINE': 32, 'AGE': '61', 'ALIVE': True}, '@I3@': {'INDI': '@I3@', 'INDI_LINE': 33, 'NAME': 'Nancy /Tsai/', 'NAME_LINE': 34, 'SEX': 'F', 'SEX_LINE': 38, 'BIRT': '1960-9-6', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F2@'], 'FAMS_LINE': 41, 'DEAT': 'NA', 'BIRT_LINE': 41, 'AGE': '59', 'ALIVE': True}, '@I4@': {'INDI': '@I4@', 'INDI_LINE': 42, 'NAME': 'Dylan /Chang/', 'NAME_LINE': 43, 'SEX': 'M', 'SEX_LINE': 47, 'BIRT': '1990-6-20', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F3@'], 'FAMS_LINE': 50, 'FAMC_LINE': 51, 'DEAT': 'NA', 'BIRT_LINE': 51, 'AGE': '29', 'ALIVE': True}, '@I5@': {'INDI': '@I5@', 'INDI_LINE': 52, 'NAME': 'Diana /Liu/', 'NAME_LINE': 53, 'SEX': 'F', 'SEX_LINE': 57, 'BIRT': '1990-8-26', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F3@'], 'FAMS_LINE': 60, 'DEAT': 'NA', 'BIRT_LINE': 60, 'AGE': '29', 'ALIVE': True}, '@I6@': {'INDI': '@I6@', 'INDI_LINE': 61, 'NAME': 'Felicia /Chang/', 'NAME_LINE': 62, 'SEX': 'F', 'SEX_LINE': 66, 'BIRT': '2010-9-8', 'INDI_CHILD': ['@F3@'], 'SPOUSE': ['@F1@'], 'FAMS_LINE': 69, 'FAMC_LINE': 70, 'DEAT': 'NA', 'BIRT_LINE': 70, 'AGE': '9', 'ALIVE': True}}
    family_dic = {'@F1@': {'FAM': '@F1@', 'FAM_LINE': 77, 'HUSB_NAME': 'David /Chang/', 'HUSB_LINE': 72, 'HUSB': '@I1@', 'WIFE_NAME': 'Felicia /Chang/', 'WIFE_LINE': 73, 'WIFE': '@I6@', 'MARR': '2012-6-12', 'DIV': 'NA', 'FAM_CHILD': 'NA', 'husband_object': {'INDI': '@I1@', 'INDI_LINE': 14, 'NAME': 'David /Chang/', 'NAME_LINE': 15, 'SEX': 'M', 'SEX_LINE': 19, 'BIRT': '1988-7-9', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F1@'], 'FAMS_LINE': 22, 'FAMC_LINE': 23, 'DEAT': 'NA', 'BIRT_LINE': 23, 'AGE': '31', 'ALIVE': True}, 'wife_object': {'INDI': '@I6@', 'INDI_LINE': 61, 'NAME': 'Felicia /Chang/', 'NAME_LINE': 62, 'SEX': 'F', 'SEX_LINE': 66, 'BIRT': '2010-9-8', 'INDI_CHILD': ['@F3@'], 'SPOUSE': ['@F1@'], 'FAMS_LINE': 69, 'FAMC_LINE': 70, 'DEAT': 'NA', 'BIRT_LINE': 70, 'AGE': '9', 'ALIVE': True}}, '@F2@': {'FAM': '@F2@', 'FAM_LINE': 85, 'HUSB_NAME': 'Johny /Chang/', 'HUSB_LINE': 79, 'HUSB': '@I2@', 'WIFE_NAME': 'Nancy /Tsai/', 'WIFE_LINE': 80, 'WIFE': '@I3@', 'FAM_CHILD': ['@I1@', '@I4@'], 'CHIL_LINE': 82, 'CHIL': '@I4@', 'MARR': '1980-3-2', 'DIV': 'NA', 'husband_object': {'INDI': '@I2@', 'INDI_LINE': 24, 'NAME': 'Johny /Chang/', 'NAME_LINE': 25, 'SEX': 'M', 'SEX_LINE': 29, 'BIRT': '1958-8-9', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F2@'], 'FAMS_LINE': 32, 'DEAT': 'NA', 'BIRT_LINE': 32, 'AGE': '61', 'ALIVE': True}, 'wife_object': {'INDI': '@I3@', 'INDI_LINE': 33, 'NAME': 'Nancy /Tsai/', 'NAME_LINE': 34, 'SEX': 'F', 'SEX_LINE': 38, 'BIRT': '1960-9-6', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F2@'], 'FAMS_LINE': 41, 'DEAT': 'NA', 'BIRT_LINE': 41, 'AGE': '59', 'ALIVE': True}, 'children_objects': [{'INDI': '@I1@', 'INDI_LINE': 14, 'NAME': 'David /Chang/', 'NAME_LINE': 15, 'SEX': 'M', 'SEX_LINE': 19, 'BIRT': '1988-7-9', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F1@'], 'FAMS_LINE': 22, 'FAMC_LINE': 23, 'DEAT': 'NA', 'BIRT_LINE': 23, 'AGE': '31', 'ALIVE': True}, {'INDI': '@I4@', 'INDI_LINE': 42, 'NAME': 'Dylan /Chang/', 'NAME_LINE': 43, 'SEX': 'M', 'SEX_LINE': 47, 'BIRT': '1990-6-20', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F3@'], 'FAMS_LINE': 50, 'FAMC_LINE': 51, 'DEAT': 'NA', 'BIRT_LINE': 51, 'AGE': '29', 'ALIVE': True}]}, '@F3@': {'FAM': '@F3@', 'FAM_LINE': 90, 'HUSB_NAME': 'Dylan /Chang/', 'HUSB_LINE': 87, 'HUSB': '@I4@', 'WIFE_NAME': 'Diana /Liu/', 'WIFE_LINE': 88, 'WIFE': '@I5@', 'FAM_CHILD': ['@I6@'], 'CHIL_LINE': 89, 'CHIL': '@I6@', 'DIV': 'NA', 'MARR': 'NA', 'husband_object': {'INDI': '@I4@', 'INDI_LINE': 42, 'NAME': 'Dylan /Chang/', 'NAME_LINE': 43, 'SEX': 'M', 'SEX_LINE': 47, 'BIRT': '1990-6-20', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F3@'], 'FAMS_LINE': 50, 'FAMC_LINE': 51, 'DEAT': 'NA', 'BIRT_LINE': 51, 'AGE': '29', 'ALIVE': True}, 'wife_object': {'INDI': '@I5@', 'INDI_LINE': 52, 'NAME': 'Diana /Liu/', 'NAME_LINE': 53, 'SEX': 'F', 'SEX_LINE': 57, 'BIRT': '1990-8-26', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F3@'], 'FAMS_LINE': 60, 'DEAT': 'NA', 'BIRT_LINE': 60, 'AGE': '29', 'ALIVE': True}, 'children_objects': [{'INDI': '@I6@', 'INDI_LINE': 61, 'NAME': 'Felicia /Chang/', 'NAME_LINE': 62, 'SEX': 'F', 'SEX_LINE': 66, 'BIRT': '2010-9-8', 'INDI_CHILD': ['@F3@'], 'SPOUSE': ['@F1@'], 'FAMS_LINE': 69, 'FAMC_LINE': 70, 'DEAT': 'NA', 'BIRT_LINE': 70, 'AGE': '9', 'ALIVE': True}]}}
    sprint2.individuals = individuals
    sprint2.family_dic = family_dic
    
    assert sprint2.is_uncle_aunt_marriage_legal() == False
    return True


# US 32 Multiple birth pass
def test_multiple_birth_pass():
    family_dic = {'@F3@': {'FAM': '@F3@',
      'FAM_LINE': 365,
      'HUSB_NAME': 'Johnny /Malagon/',
      'HUSB_LINE': 366,
      'HUSB': '@I16@',
      'WIFE_NAME': 'Lura /Lomas/',
      'WIFE_LINE': 367,
      'WIFE': '@I17@',
      'FAM_CHILD': ['@I2@',
       '@I18@',
       '@I20@',
       '@I21@',
       '@I22@',
       '@I23@',
       '@I24@',
       '@I25@',
       '@I26@',
       '@I27@',
       '@I28@',
       '@I29@',
       '@I30@',
       '@I31@',
       '@I32@',
       '@I33@'],
      'CHIL_LINE_@I2@': 368,
      'CHIL': '@I33@',
      'CHIL_LINE': 383,
      'CHIL_LINE_@I18@': 369,
      'CHIL_LINE_@I20@': 370,
      'CHIL_LINE_@I21@': 371,
      'CHIL_LINE_@I22@': 372,
      'CHIL_LINE_@I23@': 373,
      'CHIL_LINE_@I24@': 374,
      'CHIL_LINE_@I25@': 375,
      'CHIL_LINE_@I26@': 376,
      'CHIL_LINE_@I27@': 377,
      'CHIL_LINE_@I28@': 378,
      'CHIL_LINE_@I29@': 379,
      'CHIL_LINE_@I30@': 380,
      'CHIL_LINE_@I31@': 381,
      'CHIL_LINE_@I32@': 382,
      'CHIL_LINE_@I33@': 383,
      'MARR_LINE': 384,
      'MARR': '1925-4-28',
      'DIV': 'NA',
      'husband_object': {'INDI': '@I16@',
       'INDI_LINE': 158,
       'NAME': 'Johnny /Malagon/',
       'NAME_LINE': 159,
       'SEX': 'M',
       'SEX_LINE': 163,
       'BIRT_LINE': 164,
       'BIRT': '1901-7-14',
       'INDI_CHILD': 'NA',
       'SPOUSE': ['@F3@'],
       'FAMS_LINE': 166,
       'DEAT': 'NA',
       'AGE': '118',
       'ALIVE': True},
      'wife_object': {'INDI': '@I17@',
       'INDI_LINE': 167,
       'NAME': 'Lura /Lomas/',
       'NAME_LINE': 168,
       'SEX': 'F',
       'SEX_LINE': 172,
       'BIRT_LINE': 173,
       'BIRT': '1900-8-30',
       'INDI_CHILD': 'NA',
       'SPOUSE': ['@F3@'],
       'FAMS_LINE': 175,
       'DEAT': 'NA',
       'AGE': '119',
       'ALIVE': True},
      'children_objects': [{'INDI': '@I2@',
        'INDI_LINE': 24,
        'NAME': 'Stephan /Malagon/',
        'NAME_LINE': 25,
        'SEX': 'M',
        'SEX_LINE': 29,
        'BIRT_LINE': 30,
        'BIRT': '1930-8-21',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': ['@F2@'],
        'FAMS_LINE': 32,
        'FAMC_LINE': 33,
        'DEAT': 'NA',
        'AGE': '89',
        'ALIVE': True},
       {'INDI': '@I18@',
        'INDI_LINE': 176,
        'NAME': 'Tesha /Malagon/',
        'NAME_LINE': 177,
        'SEX': 'F',
        'SEX_LINE': 181,
        'BIRT_LINE': 182,
        'BIRT': '1819-7-8',
        'DEAT_LINE': 184,
        'DEAT': '2019-8-2',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 186,
        'AGE': '200',
        'ALIVE': False},
       {'INDI': '@I20@',
        'INDI_LINE': 196,
        'NAME': 'Lucile /Malagon/',
        'NAME_LINE': 197,
        'SEX': 'F',
        'SEX_LINE': 201,
        'BIRT_LINE': 202,
        'BIRT': '1931-9-9',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 204,
        'DEAT': 'NA',
        'AGE': '88',
        'ALIVE': True},
       {'INDI': '@I21@',
        'INDI_LINE': 205,
        'NAME': 'Regena /Malagon/',
        'NAME_LINE': 206,
        'SEX': 'F',
        'SEX_LINE': 210,
        'BIRT_LINE': 211,
        'BIRT': '1820-10-8',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 213,
        'DEAT': 'NA',
        'AGE': '199',
        'ALIVE': True},
       {'INDI': '@I22@',
        'INDI_LINE': 214,
        'NAME': 'Tom /Malagon/',
        'NAME_LINE': 215,
        'SEX': 'M',
        'SEX_LINE': 219,
        'BIRT_LINE': 220,
        'BIRT': '1923-5-8',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': ['@F9@'],
        'FAMS_LINE': 222,
        'FAMC_LINE': 223,
        'DEAT': 'NA',
        'AGE': '96',
        'ALIVE': True},
       {'INDI': '@I23@',
        'INDI_LINE': 224,
        'NAME': 'Vonnie /Malagon/',
        'NAME_LINE': 225,
        'SEX': 'M',
        'SEX_LINE': 229,
        'BIRT_LINE': 230,
        'BIRT': '1936-3-10',
        'DEAT_LINE': 232,
        'DEAT': '1937-7-6',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 234,
        'AGE': '1',
        'ALIVE': False},
       {'INDI': '@I24@',
        'INDI_LINE': 235,
        'NAME': 'Shena /Malagon/',
        'NAME_LINE': 236,
        'SEX': 'F',
        'SEX_LINE': 240,
        'BIRT_LINE': 241,
        'BIRT': '1937-11-6',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 243,
        'DEAT': 'NA',
        'AGE': '81',
        'ALIVE': True},
       {'INDI': '@I25@',
        'INDI_LINE': 244,
        'NAME': 'Hailey /Malagon/',
        'NAME_LINE': 245,
        'SEX': 'F',
        'SEX_LINE': 249,
        'BIRT_LINE': 250,
        'BIRT': '1938-10-8',
        'DEAT_LINE': 252,
        'DEAT': '1939-9-18',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 254,
        'AGE': '0',
        'ALIVE': False},
       {'INDI': '@I26@',
        'INDI_LINE': 255,
        'NAME': 'Milford /Malagon/',
        'NAME_LINE': 256,
        'SEX': 'M',
        'SEX_LINE': 260,
        'BIRT_LINE': 261,
        'BIRT': '1939-11-8',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 263,
        'DEAT': 'NA',
        'AGE': '79',
        'ALIVE': True},
       {'INDI': '@I27@',
        'INDI_LINE': 264,
        'NAME': 'Rashida /Malagon/',
        'NAME_LINE': 265,
        'SEX': 'F',
        'SEX_LINE': 269,
        'BIRT_LINE': 270,
        'BIRT': '1940-12-7',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 272,
        'DEAT': 'NA',
        'AGE': '78',
        'ALIVE': True},
       {'INDI': '@I28@',
        'INDI_LINE': 273,
        'NAME': 'Deeann /Malagon/',
        'NAME_LINE': 274,
        'SEX': 'F',
        'SEX_LINE': 278,
        'BIRT_LINE': 279,
        'BIRT': '1941-10-23',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 281,
        'DEAT': 'NA',
        'AGE': '77',
        'ALIVE': True},
       {'INDI': '@I29@',
        'INDI_LINE': 282,
        'NAME': 'Dario /Malagon/',
        'NAME_LINE': 283,
        'SEX': 'M',
        'SEX_LINE': 287,
        'BIRT_LINE': 288,
        'BIRT': '1942-12-14',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 290,
        'DEAT': 'NA',
        'AGE': '76',
        'ALIVE': True},
       {'INDI': '@I30@',
        'INDI_LINE': 291,
        'NAME': 'Chet /Malagon/',
        'NAME_LINE': 292,
        'SEX': 'M',
        'SEX_LINE': 296,
        'BIRT_LINE': 297,
        'BIRT': '1943-8-18',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 299,
        'DEAT': 'NA',
        'AGE': '76',
        'ALIVE': True},
       {'INDI': '@I31@',
        'INDI_LINE': 300,
        'NAME': 'Sock /Malagon/',
        'NAME_LINE': 301,
        'SEX': 'F',
        'SEX_LINE': 305,
        'BIRT_LINE': 306,
        'BIRT': '1955-10-17',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 308,
        'DEAT': 'NA',
        'AGE': '63',
        'ALIVE': True},
       {'INDI': '@I32@',
        'INDI_LINE': 309,
        'NAME': 'Chet /Malagon/',
        'NAME_LINE': 310,
        'SEX': 'M',
        'SEX_LINE': 314,
        'BIRT_LINE': 315,
        'BIRT': '1943-8-18',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 317,
        'DEAT': 'NA',
        'AGE': '76',
        'ALIVE': True},
       {'INDI': '@I33@',
        'INDI_LINE': 318,
        'NAME': 'Loyd /Malagon/',
        'NAME_LINE': 319,
        'SEX': 'M',
        'SEX_LINE': 323,
        'BIRT_LINE': 324,
        'BIRT': '1965-8-9',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 326,
        'DEAT': 'NA',
        'AGE': '54',
        'ALIVE': True}]}}
    
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []
    sprint2.multiple_birth()

    return sprint2.anomaly_array==['ANOMALY: FAMILY: US32: 365: The two or more individuals were born at the same time in a family @F3@']
    return True
    
# US32 Multiple birth fail
def test_multiple_birth_fail():
    family_dic = {'@F3@': {'FAM': '@F3@',
      'HUSB_NAME': 'Johnny /Malagon/',
      'HUSB': '@I16@',
      'WIFE_NAME': 'Lura /Lomas/',
      'WIFE': '@I17@',
      'FAM_CHILD': ['@I30@',
       '@I31@'],
      'CHIL': '@I34@',
      'MARR': '1925-4-28',
      'DIV': 'NA',
      'husband_object': {'INDI': '@I16@',
       'NAME': 'Johnny /Malagon/',
       'SEX': 'M',
       'BIRT': '1901-7-14',
       'INDI_CHILD': 'NA',
       'SPOUSE': ['@F3@'],
       'DEAT': 'NA',
       'AGE': '118',
       'ALIVE': True},
      'wife_object': {'INDI': '@I17@',
       'NAME': 'Lura /Lomas/',
       'SEX': 'F',
       'BIRT': '1900-8-30',
       'INDI_CHILD': 'NA',
       'SPOUSE': ['@F3@'],
       'DEAT': 'NA',
       'AGE': '119',
       'ALIVE': True},
      'children_objects': [{'INDI': '@I30@',
        'INDI_LINE': 291,
        'NAME': 'Chet /Malagon/',
        'NAME_LINE': 292,
        'SEX': 'M',
        'SEX_LINE': 296,
        'BIRT_LINE': 297,
        'BIRT': '1943-8-18',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 299,
        'DEAT': 'NA',
        'AGE': '76',
        'ALIVE': True},
       {'INDI': '@I31@',
        'INDI_LINE': 300,
        'NAME': 'Sock /Malagon/',
        'NAME_LINE': 301,
        'SEX': 'F',
        'SEX_LINE': 305,
        'BIRT_LINE': 306,
        'BIRT': '1955-10-17',
        'INDI_CHILD': ['@F3@'],
        'SPOUSE': 'NA',
        'FAMC_LINE': 308,
        'DEAT': 'NA',
        'AGE': '63',
        'ALIVE': True}]}}
    
    
    sprint2.family_dic = family_dic
    sprint2.anomaly_array = []
    sprint2.multiple_birth()

    return len(sprint2.anomaly_array) == 0
    return True


class TestUserStory(unittest.TestCase):
    """ Test case for user story """


    def test_Dates_After_Today_error(self):
        """ Test case for user story 1 to check for Date before current date """
        self.assertFalse(test_dates_error('2021-05-15','2022-02-20','2021-06-17','2022-07-25'))
        self.assertFalse(test_dates_error('2022-05-15','2024-05-25','2051-06-17','2022-07-25'))

    def test_Dates_After_Today_pass(self):
        """ Test case for user story 1 to check for Date before current date """
        self.assertTrue(test_dates_pass('2015-06-12','2019-05-11','1972-02-10','1975-03-15'))
        self.assertTrue(test_dates_pass('2015-04-12','2020-04-16','1999-02-10','2002-07-16'))
        self.assertTrue(test_dates_pass('2012-06-12','2018-05-11','1965-02-10','1970-04-15'))
      
    def test_Birth_After_Marraige_Appended_To_Error(self):
        """Test Case for user story 02 to check birth before marriage error"""
        self.assertTrue(test_birth_after_marraige_appended_to_error())
    def test_Birth_Before_Marraige_Do_Nothing(self):
        """Test Case for user story 2"""
        self.assertTrue(test_birth_before_marraige_do_nothing())

    def test_Less_Than_15_Siblings_pass(self):
        """Test Case for user story 15"""
        d1 = {'@F1@':{'FAM_CHILD':['@I1@']}}
        d2 = {'@F1@':{'FAM_CHILD':['@I1@', '@I2@', '@I3@']}}
        d3 = {'@F1@':{'FAM_CHILD':['@I1@', '@I2@', '@I3@', '@I4@', '@I5@']}}
        d4 = {'@F1@':{'FAM_CHILD':['@I1@', '@I2@', '@I3@', '@I4@']}}
        d5 = {'@F1@':{'FAM_CHILD':['@I1@', '@I2@']}}

        self.assertTrue(test_less_than_15_siblings(d1))
        self.assertTrue(test_less_than_15_siblings(d2))
        self.assertTrue(test_less_than_15_siblings(d3))
        self.assertTrue(test_less_than_15_siblings(d4))
        self.assertTrue(test_less_than_15_siblings(d5))

    def test_Less_Than_15_Siblings_fail(self):
        """Test Case for user story 15"""
        d1 = {'@F1@':{'FAM_CHILD':['@I1@', '@I2@', '@I3@', '@I4@', '@I5@', '@I6@', '@I7@', '@I8@', '@I9@', '@I10@', '@I11@', '@I12@', '@I13@', '@I14@', '@I15@', '@I16@']}}

        self.assertFalse(test_less_than_15_siblings(d1))
    
    def test_unique_family_name_and_birth_pass(self):
        """Test Case for user story 23"""
        self.assertTrue(test_unique_family_name_and_birth_pass())

    def test_unique_family_name_and_birth_error(self):
        """Test Case for user story 23"""
        self.assertTrue(test_unique_family_name_and_birth_error())

    def test_unique_name_and_birth_pass(self):
        """Test Case for user story 23"""
        self.assertTrue(test_unique_name_and_birth_pass(1955))

    def test_unique_name_and_birth_fail(self):
        """Test Case for user story 23"""
        self.assertFalse(test_unique_name_and_birth_pass(1954))
        self.assertFalse(test_unique_name_and_birth_pass(1934))
        self.assertFalse(test_unique_name_and_birth_pass(1924))
        self.assertFalse(test_unique_name_and_birth_pass(1964))
        self.assertFalse(test_unique_name_and_birth_pass(1974))

    def test_Different_Male_Last_Name(self):
        """Test Case for user story 16"""
        self.assertTrue(test_different_male_last_name())


    def test_Same_Male_Last_Name(self):
        """Test Case for user story 16"""
        self.assertTrue(test_same_male_last_name())

    def test_List_Deceased_success(self):
        """Test Case for user story 29"""
        self.assertTrue(test_list_deceased_individuals_success())
		
    def test_List_Deceased_fail(self):
        """Test Case for user story 29"""
        self.assertTrue(test_list_deceased_individuals_error())
		
    def test_List_Living_Married_success(self):
        """Test Case for user story 30"""
        self.assertTrue(test_list_living_married_individuals_success())
		
    def test_List_Living_Married_fail(self):
        """Test Case for user story 30"""
        self.assertTrue(test_list_living_married_individuals_error())
	
    def test_Marriqge_Ater_14_pass(self):
        """Test Case for user story 10"""
        self.assertTrue(test_legal_marriage(1972))
        self.assertTrue(test_legal_marriage(1974))
        self.assertTrue(test_legal_marriage(1971))
        self.assertTrue(test_legal_marriage(1980))
        self.assertTrue(test_legal_marriage(1981))

    def test_Marriqge_Ater_14_fail(self):
        """Test Case for user story 10"""
        self.assertFalse(test_legal_marriage(2004))
        self.assertFalse(test_legal_marriage(2005))
        self.assertFalse(test_legal_marriage(2006))
        self.assertFalse(test_legal_marriage(2007))
        self.assertFalse(test_legal_marriage(2008))

    def test_Less_Then_150_Years_Old_fail(self):
        """Test Case for user story 07"""
        self.assertTrue(test_over_age_150())
        
    def test_Less_Then_150_Years_Old_pass(self):
        """Test Case for user story 07"""
        self.assertTrue(test_less_age_150())

    def test_birth_before_parents_marriage_fail(self):
        """ Test case for user story 8 to check if childrens are born after marriage of parents (fail) """
        self.assertTrue(test_birth_before_marriage_fail())

    def test_birth_before_parents_marriage_pass(self):
        """ Test case for user story 8 to check if childrens are born after marriage of parents (pass)  """
        self.assertTrue(test_birth_before_marriage_pass())

    def test_birth_before_death_fail(self):
        """ Test case for user story 9 to check if child is born before death of mother and before 9 months after death of father (fail) """
        self.assertTrue(test_birth_before_death_fail())

    def test_birth_before_death_pass(self):
        """ Test case for user story 9 to check if child is born before death of mother and before 9 months after death of father (pass) """
        self.assertTrue(test_birth_before_death_pass())

    def test_aunts_and_uncles_pass(self):
        """ Test case US 20"""
        self.assertTrue(aunts_and_uncles_success())

    def test_aunts_and_uncles_fail(self):
        """ Test case US 20"""
        self.assertTrue(aunts_and_uncles_error())

    def test_multiple_birth_pass(self):
        """Test Case US32 """
        self.assertTrue(test_multiple_birth_pass())

    def test_multiple_birth_fail(self):
        """Test Case US32 """
        self.assertTrue(test_multiple_birth_fail())



	
	
if __name__ == '__main__':
    """ Run test cases on startup """
    unittest.main(exit=False, verbosity=2)