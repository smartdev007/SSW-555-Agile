import unittest
import sprint1
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
    
    sprint1.family_dic = family_dic
    sprint1.anomaly_array = []
    sprint1.is_marriage_legal()

    return len(sprint1.anomaly_array) == 0

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
                    
    sprint1.individuals = individuals
    sprint1.anomaly_array = []
    sprint1.is_age_legal()
    
    return sprint1.anomaly_array==['ANOMALY: INDIVIDUAL: US07: @I1@: More than 150 years old - Birth Date 1860-6-5',
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
                    
    sprint1.individuals = individuals
    sprint1.anomaly_array = []
    sprint1.is_age_legal()
    
    return len(sprint1.anomaly_array) == 0


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
    
    sprint1.family_dic = family_dic
    sprint1.individuals=individuals
    sprint1.anomaly_array = []
    sprint1.validate_dates()

    return len(sprint1.anomaly_array)==0


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
    
    sprint1.family_dic = family_dic
    sprint1.individuals=individuals
    sprint1.anomaly_array = []
    sprint1.validate_dates()

    return sprint1.anomaly_array==[f'ERROR: FAMILY: US01: @F8@: Family has marrige date {date} later than today',
                                 f'ERROR: FAMILY: US01: @F8@: Family has divorce date {ddate} later than today',
                                 f'ERROR: INDIVIDUAL: US01: @I1@: Individual has birth date {bdate} later than today']

def test_birth_before_marraige_do_nothing():
    family_dic = {'@F1@':{'MARR':'1968-6-4','husband_object':{'INDI':'@I1@','BIRT':'1950-11-8'},'wife_object':{'INDI':'@I2@','BIRT':'1960-11-8'}}}
    sprint1.family_dic = family_dic
    sprint1.anomaly_array = []
    
    sprint1.is_birth_before_marraige()
    
    assert len(sprint1.anomaly_array) == 0
    return True


def test_birth_after_marraige_appended_to_error():
    family_dic = {'@F1@':{'MARR':'1968-6-4','husband_object':{'INDI':'@I1@','BIRT':'1970-11-8'},'wife_object':{'INDI':'@I2@','BIRT':'1960-11-8'}}}
    sprint1.family_dic = family_dic
    sprint1.anomaly_array = []
    
    sprint1.is_birth_before_marraige()
    
    assert sprint1.anomaly_array[0] == "ERROR: INDIVIDUAL: US02: @I1@: Person has marriage date 1968-6-4 before birth date 1970-11-8"
    return True

# User_Story_29: List all deceased individuals in a GEDCOM file
# Success test 
@mock.patch("sprint1.printTable")
def test_list_deceased_individuals_success(mock_printTable):
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT"]
    current_dic = {'@I6@': {'INDI': '@I6@', 'NAME': 'Stephen /Chang/', 'SEX': 'M', 'BIRT': '1935-12-5', 'DEAT': '2005-4-15', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F2@'], 'AGE': '70', 'ALIVE': False}}
    sprint1.individuals = current_dic
    sprint1.listDeceased()
    mock_printTable.assert_called_with("US29: Deceased People Table", allFields, tagNames, current_dic)
    return True

	
# User_Story_29: List all deceased individuals in a GEDCOM file
# Failed test: Person is dead but has no Death Date
@mock.patch("sprint1.printTable")
def test_list_deceased_individuals_error(mock_printTable):
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT"]
    current_dic = {'@I6@': {'INDI': '@I6@', 'NAME': 'David /Chang/', 'SEX': 'M', 'BIRT': '2002-12-5', 'DEAT': 'NA', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F7@'], 'AGE': '79', 'ALIVE': False}}
    sprint1.individuals = current_dic
    sprint1.listDeceased()
    mock_printTable.assert_called_with("US29: Deceased People Table", allFields, tagNames, {}) #provide empty dictionary so that it won't overwrite
    return True
	
# User_Story_30: List all living married people in a GEDCOM file
# Success test
@mock.patch("sprint1.printTable")
def test_list_living_married_individuals_success(mock_printTable):

    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]
    current_dic = {'@I1@': {'INDI': '@I1@', 'NAME': 'Johnny /Chang/', 'SEX': 'M', 'BIRT': '1958-9-6', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F1@'], 'DEAT': 'NA', 'AGE': '61', 'ALIVE': True}}
    sprint1.individuals = current_dic
    sprint1.listLivingMarried()
    mock_printTable.assert_called_with("US30: Living & Married People Table", allFields, tagNames, current_dic)
    return True

# User_Story_30: List all living married people in a GEDCOM file
# Failed test
@mock.patch("sprint1.printTable")
def test_list_living_married_individuals_error(mock_printTable):
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]
    current_dic = {'@I4@': {'INDI': '@I1@', 'NAME': 'Michael /Chang/', 'SEX': 'M', 'BIRT': '1958-9-6', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F3@'], 'DEAT': '2002-9-6', 'AGE': '61', 'ALIVE': False}}
    sprint1.individuals = current_dic
    sprint1.listLivingMarried()
    mock_printTable.assert_called_with("US30: Living & Married People Table", allFields, tagNames, {}) #provide empty dictionary so that it won't overwrite
    return True


def test_less_than_15_siblings(sib_dic):
    family_dic = sib_dic
    sprint1.family_dic = family_dic
    sprint1.anomaly_array = []
    
    sprint1.check_sibling_count()

    return len(sprint1.anomaly_array) == 0

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
    
    sprint1.family_dic = family_dic
    sprint1.anomaly_array = []
    sprint1.unique_family_name_and_birth()

    return sprint1.anomaly_array==['ANOMALY: INDIVIDUAL: US25: @I13@: @I7@: Individuals share the same name Beth /Venzon/ and birth date 1973-7-8 from family @F1@']

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
    
    sprint1.family_dic = family_dic
    sprint1.anomaly_array = []
    sprint1.unique_family_name_and_birth()

    return len(sprint1.anomaly_array) == 0


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

    sprint1.individuals = individuals
    sprint1.anomaly_array = []

    sprint1.unique_name_and_birth()

    return sprint1.anomaly_array == [
        'ANOMALY: INDIVIDUAL: US23: @I35@: @I31@: Individuals have the same name Sock /Malagon/ and birth date 1955-10-17']


def test_different_male_last_name():
    family_dic = {'@F1@': {'HUSB_NAME': 'Harry /Potter/', 'FAM_CHILD': ['@I1@', '@I10@'],
                           'children_objects': [{'INDI': '@I1@', 'SEX': 'M', 'NAME': 'Chandler /Bing/'},
                                                {'INDI': '@I10@', 'SEX': 'M', 'NAME': 'Chandler /Potter/'}]}}
    sprint1.family_dic = family_dic
    sprint1.anomaly_array = []

    sprint1.check_last_names()
    return sprint1.anomaly_array[
               0] == 'ANOMALY: INDIVIDUAL: US16: @I1@: Individual has different last name Bing than family Potter'


def test_same_male_last_name():
    family_dic = {'@F1@': {'HUSB_NAME': 'Harry /Potter/', 'FAM_CHILD': ['@I1@', '@I10@'],
                           'children_objects': [{'INDI': '@I1@', 'SEX': 'M', 'NAME': 'Joey /Potter/'},
                                                {'INDI': '@I10@', 'SEX': 'M', 'NAME': 'Chandler /Potter/'}]}}
    sprint1.family_dic = family_dic
    sprint1.anomaly_array = []

    sprint1.check_last_names()

    return len(sprint1.anomaly_array) == 0



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


	
	
if __name__ == '__main__':
    """ Run test cases on startup """
    unittest.main(exit=False, verbosity=2)
