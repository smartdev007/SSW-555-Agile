import unittest
import sprint1
import mock



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
@mock.patch("Sprint1.printTable")
def test_list_deceased_individuals_success(mock_printTable):
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT"]
    current_dic = {'@I6@': {'INDI': '@I6@', 'NAME': 'Stephen /Chang/', 'SEX': 'M', 'BIRT': '1935-12-5', 'DEAT': '2005-4-15', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F2@'], 'AGE': '70', 'ALIVE': False}}
    Sprint1.individuals = current_dic
    Sprint1.listDeceased()
    mock_printTable.assert_called_with("US29: Deceased People Table", allFields, tagNames, current_dic)
    return True

	
# User_Story_29: List all deceased individuals in a GEDCOM file
# Failed test: Person is dead but has no Death Date
@mock.patch("Sprint1.printTable")
def test_list_deceased_individuals_error(mock_printTable):
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT"]
    current_dic = {'@I6@': {'INDI': '@I6@', 'NAME': 'David /Chang/', 'SEX': 'M', 'BIRT': '2002-12-5', 'DEAT': 'NA', 'INDI_CHILD': 'NA', 'SPOUSE': ['@F7@'], 'AGE': '79', 'ALIVE': False}}
    Sprint1.individuals = current_dic
    Sprint1.listDeceased()
    mock_printTable.assert_called_with("US29: Deceased People Table", allFields, tagNames, {}) #provide empty dictionary so that it won't overwrite
    return True
	
# User_Story_30: List all living married people in a GEDCOM file
# Success test
@mock.patch("Sprint1.printTable")
def test_list_living_married_individuals_success(mock_printTable):

    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]
    current_dic = {'@I1@': {'INDI': '@I1@', 'NAME': 'Johnny /Chang/', 'SEX': 'M', 'BIRT': '1958-9-6', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F1@'], 'DEAT': 'NA', 'AGE': '61', 'ALIVE': True}}
    Sprint1.individuals = current_dic
    Sprint1.listLivingMarried()
    mock_printTable.assert_called_with("US30: Living & Married People Table", allFields, tagNames, current_dic)
    return True


	
# User_Story_30: List all living married people in a GEDCOM file
# Failed test
@mock.patch("Sprint1.printTable")
def test_list_living_married_individuals_error(mock_printTable):
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]
    current_dic = {'@I4@': {'INDI': '@I1@', 'NAME': 'Michael /Chang/', 'SEX': 'M', 'BIRT': '1958-9-6', 'INDI_CHILD': ['@F2@'], 'SPOUSE': ['@F3@'], 'DEAT': '2002-9-6', 'AGE': '61', 'ALIVE': False}}
    Sprint1.individuals = current_dic
    Sprint1.listLivingMarried()
    mock_printTable.assert_called_with("US30: Living & Married People Table", allFields, tagNames, {}) #provide empty dictionary so that it won't overwrite
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
        self.assertTrue(test_birth_after_marraige_appended_to_error())
    def test_Birth_Before_Marraige_Do_Nothing(self):
        self.assertTrue(test_birth_before_marraige_do_nothing())
        
    def test_List_Deceased_success(self):
        self.assertTrue(test_list_deceased_individuals_success())
		
    def test_List_Deceased_fail(self):
        self.assertTrue(test_list_deceased_individuals_error())
		
    def test_List_Living_Married_success(self):
        self.assertTrue(test_list_living_married_individuals_success())
		
    def test_List_Living_Married_fail(self):
        self.assertTrue(test_list_living_married_individuals_error())    
        


if __name__ == '__main__':
    """ Run test cases on startup """
    unittest.main(exit=False, verbosity=2)
