from datetime import datetime
from datetime import date
from prettytable import PrettyTable
import re

def_tag = ["INDI", "FAM"]

header_tag = ["HEAD", "TRLR", "NOTE"]

supported_tag = ["NAME", "SEX", "BIRT", "DEAT","FAMC","FAMS","MARR", "DIV","HUSB","WIFE","CHIL"]

dict_tag = {"INDI": ["NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS"],
             "FAM": ["MARR", "DIV", "HUSB", "WIFE", "CHIL"],
             "DATE": ["BIRT", "DEAT", "DIV", "MARR"]}

family_dic = None
anomaly_array = []
document = {}
error_array = []

def create_individuals_map():
    global individuals
    individuals = {}

    for individual in document["INDI"]:
        individuals[individual["INDI"]] = individual

def create_family_dic():
    global family_dic
    family_dic = {}

    for family in document["FAM"]:
        if family["HUSB"] != "NA" and family["HUSB"] in individuals:
            family["husband_object"] = individuals[family["HUSB"]]

        if family["WIFE"] != "NA" and family["WIFE"] in individuals:
            family["wife_object"] = individuals[family["WIFE"]]

        if family["FAM_CHILD"] != "NA":
            children = []

            for child in family["FAM_CHILD"]:
                children.append(individuals[child])

            family["children_objects"] = children

        family_dic[family["FAM"]] = family

# create dictionary entry for the passed tag
# :param current_arr is the current array line being processed
# :param tag can will be either FAM or INDI
def create_dic_entry(current_arr, tag):
    current_tag=tag
    dic={}
    dic[tag]=current_arr[1]
    return dic, current_tag

    for family in document["FAM"]:
        if family["HUSB"] != "NA" and family["HUSB"] in individuals:
            family["husband_object"] = individuals[family["HUSB"]]

        if family["WIFE"] != "NA" and family["WIFE"] in individuals:
            family["wife_object"] = individuals[family["WIFE"]]

        if family["FAM_CHILD"] != "NA":
            children = []

            for child in family["FAM_CHILD"]:
                children.append(individuals[child])

            family["children_objects"] = children

        family_dic[family["FAM"]] = family


# Adds missing tags with "NA"
def add_missing_entries(dic):
    if "DIV" not in dic:
        dic["DIV"] = "NA"
    if "HUSB" not in dic:
        dic["HUSB"] = "NA"
    if "HUSB_NAME" not in dic:
        dic["HUSB_NAME"] = "NA"
    if "WIFE" not in dic:
        dic["WIFE"] = "NA"
    if "WIFE_NAME" not in dic:
        dic["WIFE_NAME"] = "NA"
    if "FAM_CHILD" not in dic:
        dic["FAM_CHILD"] = "NA"
    if "MARR" not in dic:
        dic["MARR"] = "NA"



#US03 - Birth Before Death - The birth of an individual SHOULD occur before his/her death

def is_birth_before_death():
    for currentIndividual in individuals.values():
        if(currentIndividual['BIRT'] == 'NA'):
            error_array.append("ERROR: INDIVIDUAL: US03: {}: Individual has no Birth Date".format(currentIndividual["INDI"]))
        elif(currentIndividual['DEAT'] != 'NA'):
            if(currentIndividual['BIRT'] > currentIndividual['DEAT']):
                error_array.append("ERROR: INDIVIDUAL: US03: {}: Individual has Birth date {} after Death Date {}".format(currentIndividual["INDI"], currentIndividual["BIRT"], currentIndividual["DEAT"]))


#USID: 06
def check_divorce_before_death():
     for family in family_dic.values():
            husband_flag=False
            wife_flag=False
            if "DIV" in family and family["DIV"]!="NA":
                divorce_date = family["DIV"]
                if "husband_object" in family and family["husband_object"] != 'NA':
                    husband=family["husband_object"]
                    if "DEAT" in husband and husband["DEAT"] != 'NA':
                        husband_flag=True
                        husband_death=husband["DEAT"]
                if "wife_object" in family and family["wife_object"] != 'NA':
                    wife=family["wife_object"]
                    if "DEAT" in wife and wife["DEAT"] != 'NA':
                        wife_flag=True
                        wife_death=wife["DEAT"]
                if husband_flag and wife_flag:
                    husband_invalid = False
                    wife_invalid = False
                    if determine_days(husband_death, divorce_date) > 0:
                        husband_invalid = True
                    if determine_days(wife_death, divorce_date) > 0:
                        wife_invalid = True
                    if husband_invalid and wife_invalid:
                        error_array.append("ERROR: FAMILY: US06: {}: {}: Divorce {} happened after the death of both spouses - Husband: {} Wife: {}.".format(family["DIV_LINE"], family["FAM"], family["DIV"], husband_death, wife_death))
                    elif husband_invalid:
                        error_array.append("ERROR: FAMILY: US06: {}: {}: Divorce {} happened after the death of husband {}.".format(family["DIV_LINE"], family["FAM"], family["DIV"], husband_death, wife_death))
                    elif wife_invalid:
                        error_array.append("ERROR: FAMILY: US06: {}: {}: Divorce {} happened after the death of wife {}.".format(family["DIV_LINE"], family["FAM"], family["DIV"], husband_death, wife_death))
                        

  

def is_marriage_legal():
    """ US10 Marriage after 14 """
    for family_id in family_dic:
        if "MARR" in family_dic[family_id] and family_dic[family_id]["MARR"]!="NA":
            married_date = family_dic[family_id]["MARR"]

        if "husband_object" in family_dic[family_id]:
            husband = family_dic[family_id]["husband_object"]

            if int(determine_age(husband["BIRT"], married_date)) < 14:
                anomaly_array.append(f"ANOMALY: INDIVIDUAL: US10: {husband['INDI']}: Father of family {family_id} is younger than 14 years old - Birth Date {husband['BIRT']}")

        if "wife_object" in family_dic[family_id]:
            wife = family_dic[family_id]["wife_object"]

            if int(determine_age(wife["BIRT"], married_date)) < 14:
                anomaly_array.append(f"ANOMALY: INDIVIDUAL: US10: {wife['INDI']}: Wife of family {family_id} is younger than 14 years old - Birth Date {wife['BIRT']}")

def is_age_legal():
    """ US07 Less than 150 years old """ 
    for indi_id in individuals:
        indi = individuals[indi_id]

        if "AGE" in indi:
            age = indi["AGE"]

            if int(age) > 150:
                if indi["ALIVE"]:
                    anomaly_array.append(f"ANOMALY: INDIVIDUAL: US07: {indi_id}: More than 150 years old - Birth Date {indi['BIRT']}")
                else:
                    anomaly_array.append(f"ANOMALY: INDIVIDUAL: US07: {indi_id}: More than 150 years old at death - Birth Date {indi['BIRT']}: Death Date {indi['DEAT']}")

def determine_days(date1, date2):
    year1=int(date1.split('-')[0])
    month1= int(date1.split('-')[1])
    day1= int(date1.split('-')[2])
    
    if date2 == None:
        year2 = int(datetime.today().strftime("%Y"))
        month2 = int(datetime.today().strftime("%m"))
        day2 = int(datetime.today().strftime("%d"))
    else:
        year2=int(date2.split('-')[0])
        month2= int(date2.split('-')[1])
        day2= int(date2.split('-')[2])
    
    return (year2 - year1) * 365 + (month2 - month1)* 30 + day2- day1

def birth_before_marriage():
    """ US08: Birth before marriage of parents """

    for family in family_dic.values():
        if "children_objects" in family:
            marriage_date = family['MARR']
            divorce_date = family["DIV"]
            for child in family["children_objects"]:
                if(marriage_date!= "NA"):
                    if(determine_days(marriage_date, child["BIRT"]) < 0):
                        anomaly_array.append(f"ANOMALY: INDIVIDUAL: US08: {child['INDI']}: Child was born at {child['BIRT']} before marriage of parents {marriage_date}")
                         
                if(divorce_date!= "NA"):
                    if(determine_days(divorce_date, child["BIRT"])/30 > 9):
                        anomaly_array.append(f"ANOMALY: INDIVIDUAL: US08: {child['INDI']}: Child was born at {child['BIRT']} after 9 month divorce of parents {divorce_date}")

def birth_before_death():
    """ US09: Birth before death of parents """

    for family in family_dic.values():
        if "children_objects" in family:
            if "husband_object" in family:
                husband_death=family["husband_object"]["DEAT"]
            if "wife_object" in family:
                wife_death=family["wife_object"]["DEAT"]
            for child in family["children_objects"]:
                if(wife_death!= "NA"):
                    if(determine_days(child["BIRT"], wife_death) < 0):
                        error_array.append(f"ERROR: INDIVIDUAL: US09: {child['INDI']}: Child was born at {child['BIRT']} after death of mother {wife_death}")
                if(husband_death!= "NA"):
                    if(determine_days(husband_death, child["BIRT"])/30 > 9):
                        error_array.append(f"ERROR: INDIVIDUAL: US09: {child['INDI']}: Child was born at {child['BIRT']} after 9 month death of father {husband_death}")




def unique_name_and_birth():
    li = {}
    for value in individuals.values():
        temp = value["NAME"] + value["BIRT"]
        if temp in li:
            anomaly_array.append("ANOMALY: INDIVIDUAL: US23: {}: {}: Individuals have the same name {} and birth date {}".format(value["INDI"], li[temp], value["NAME"], value["BIRT"]))
        else:
            li[temp]=value["INDI"]

def get_last_name(name):
    return name.split('/')[1]

def check_last_names():
    for family_id in family_dic:
        family = family_dic[family_id]
        last_name = None

        if "HUSB_NAME" in family:
            if family["HUSB_NAME"] != "NA":
                last_name = get_last_name(family["HUSB_NAME"])
            else:
                continue

        if "children_objects" in family:
            for child in family["children_objects"]:
                if child["SEX"] == "M":
                    if last_name is None:
                        last_name = get_last_name(child["NAME"])
                    else:
                        if last_name != get_last_name(child["NAME"]):
                            anomaly_array.append(f"ANOMALY: INDIVIDUAL: US16: {child['INDI']}: Individual has different last name {get_last_name(child['NAME'])} than family {last_name}")
                            
def isDateParent(A):
    return A[1] in dict_tag["DATE"]

def month_to_num(shortMonth):
    return{
        'JAN' : "1",
        'FEB' : "2",
        'MAR' : "3",
        'APR' : "4",
        'MAY' : "5",
        'JUN' : "6",
        'JUL' : "7",
        'AUG' : "8",
        'SEP' : "9", 
        'OCT' : "10",
        'NOV' : "11",
        'DEC' : "12"
    }[shortMonth]

def convert_date(date_arr):
    return f'{date_arr[2]} - {month_to_num(date_arr[1])} - {date_arr[0]}'

# Checking if one date is after another
# :param date_one is the date being compared with
# :param date_two is the date being compared t0
def is_date_after(date_one, date_two):
    return date_one < date_two


def determine_age(birth_date, death_date):
    if death_date:
        return int(death_date.split('-')[0]) - int(birth_date.split('-')[0])
    else:
        today = datetime.today()
        return today.year - int(birth_date.split('-')[0])


# USID: 01
# The Dates we need to check includes: birth, marriage, divorce, death
# Birth always exists, the rests we need to check for NA
# Iteration through individuals and family
def validate_dates():
    for family in family_dic.values():
        if family["MARR"] !="NA":
            if(determine_age(family["MARR"], None) < 0):
                 anomaly_array.append("ERROR: FAMILY: US01: {}: Family has marrige date {} later than today".format(family["FAM"], family["MARR"]))
        if family["DIV"] != "NA":
            if(determine_age(family["DIV"], None) < 0):
                 anomaly_array.append("ERROR: FAMILY: US01: {}: Family has divorce date {} later than today".format(family["FAM"], family["DIV"]))     
    
    for indi in individuals.values():
        # for birthday simply check age
        if(determine_age(indi["BIRT"], None) < 0):
                anomaly_array.append("ERROR: INDIVIDUAL: US01: {}: Individual has birth date {} later than today".format(indi["INDI"], indi["BIRT"]))     
        if indi["DEAT"] != "NA":
            if(determine_age(indi["DEAT"], None) < 0):
                anomaly_array.append("ERROR: INDIVIDUAL: US01: {}: Individual has death date {} later than today".format(indi["INDI"], indi["DEAT"]))  

#USID: 02
# This function checks if the birth of the person is before their 
# marriage date
# If birth of the person is after the marriage date then the error
# is appended to the error array
def is_birth_before_marraige():
    for family_id in family_dic:
        family = family_dic[family_id]
        if "MARR" in family:
            marriage_date = family["MARR"]
            husband_birth_date = None
            wife_birth_date = None
            if "husband_object" in family and "BIRT" in family["husband_object"]:
                husband_birth_date = family["husband_object"]["BIRT"]
            else:
                continue
            if "wife_object" in family and "BIRT" in family["wife_object"]:
                wife_birth_date = family["wife_object"]["BIRT"]
            else:
                continue
            if is_date_after(marriage_date, husband_birth_date):
                anomaly_array.append(("ERROR: INDIVIDUAL: US02: {}: Person has marriage date {} before birth date {}").format(family["husband_object"]["INDI"], marriage_date, husband_birth_date))
            if is_date_after(marriage_date, wife_birth_date):
                anomaly_array.append(("ERROR: INDIVIDUAL: US02: {}: Person has marriage date {} before birth date {}")                                    .format(family["wife_object"]["INDI"], marriage_date, wife_birth_date))


#USID: 15
# This function checks sibling count
def check_sibling_count():
    for family_id in family_dic:
        family = family_dic[family_id]
        if (len(family["FAM_CHILD"]) > 15):
            anomaly_array.append("ANOMALY: FAMILY: US16: {}: Family has {} siblings which is more than 15 siblings")  


# USID: 11
def check_for_bigamy():
    for individual_id in individuals:
        individual = individuals[individual_id]
        if "SPOUSE" in individual and individual["SPOUSE"] != 'NA':
            spouse_in_families = individual["SPOUSE"]
            if len(spouse_in_families) > 1:
                dates = []
                for family_id in spouse_in_families:
                    family = family_dic[family_id]
                    date = {}
                    if "MARR" in family and family["MARR"] != 'NA':
                        date["MARR"] = family["MARR"]
                    if "DIV" in family and family["DIV"] != 'NA':
                        date["DIV"] = family["DIV"]
                    elif "husband_object" in family and family["husband_object"] != 'NA':
                        if "DEAT" in family["husband_object"] and family["husband_object"]["DEAT"] != 'NA':
                            date["DIV"] = family["husband_object"]["DEAT"]
                    dates.append(date)
                if compare_marraige_dates(dates):
                    anomaly_array.append("ANOMALY: INDIVIDUAL: US11: {}: {}: Performing bigamy".format(individual["INDI_LINE"], individual["INDI"]))


def compare_marraige_dates(dates):
    for i in range(0, len(dates)):
        dateOne = dates[i]
        for j in range(i + 1, len(dates)):
            dateTwo = dates[j]
            if "MARR" in dateOne and "DIV" in dateOne:
                if "MARR" in dateTwo:
                    if dateOne["MARR"] <= dateTwo["MARR"] < dateOne["DIV"]:
                        return True
                if "DIV" in dateTwo:
                    if dateOne["MARR"] < dateTwo["DIV"] < dateOne["DIV"]:
                        return True
            elif "MARR" in dateOne:
                if "MARR" in dateTwo and "DIV" in dateTwo:
                    if dateTwo["MARR"] <= dateOne["MARR"] < dateTwo["DIV"]:
                        return True
                if "MARR" in dateTwo and dateOne["MARR"] <= dateTwo["MARR"]:
                    return True
                if "DIV" in dateTwo and dateOne["MARR"] < dateTwo["DIV"]:
                    return True
                if "MARR" in dateTwo and "DIV" not in dateTwo and dateTwo["MARR"] <= dateOne["MARR"]:
                    return True
            elif "DIV" in dateOne:
                if "MARR" in dateTwo and "DIV" in dateTwo:
                    if dateTwo["MARR"] <= dateOne["DIV"] < dateTwo["DIV"]:
                        return True
    return False


def check_parent_child_marriage():
    for family_id in family_dic:
        family = family_dic[family_id]
        if "HUSB" in family and family["HUSB"] != 'NA' and "WIFE" in family and family["WIFE"] != 'NA':
            if is_spouse_a_child(family["HUSB"], family["WIFE"]):
                anomaly_array.append("ANOMALY: INDIVIDUAL: US17: {}: {}: Individual married to child {}"\
                                    .format(family["HUSB_LINE"], family["HUSB"], family["WIFE"]))
            if is_spouse_a_child(family["WIFE"], family["HUSB"]):
                anomaly_array.append("ANOMALY: INDIVIDUAL: US17: {}: {}: Individual married to child {}"\
                                    .format(family["WIFE_LINE"], family["WIFE"], family["HUSB"]))


def is_spouse_a_child(individual_id, spouse_id):
    individual_object = individuals[individual_id]
    if 'SPOUSE' in individual_object and individual_object['SPOUSE'] != 'NA':
        for spouse_fam in individual_object['SPOUSE']:
            if spouse_fam in family_dic:
                family = family_dic[spouse_fam]
                if "FAM_CHILD" in family and spouse_id in family["FAM_CHILD"]:
                    return True
        return False


#User_Story_20 Aunts and uncles
#Aunts and uncles should not marry their nieces or nephews
def is_uncle_aunt_marriage_legal():
    for indi in individuals.values(): #scans through each individual first
        current_sp = indi["SPOUSE"] #Array of spouse's family IDs
        current_fm = indi["INDI_CHILD"] #gets the family ID that the person belongs to
        if (current_sp != "NA" and current_fm != "NA"): #if the person has a spouse
            for fam_id in current_fm: #scans through uncle's families
                current_family = family_dic[fam_id]
                current_siblings = current_family["children_objects"] #get the uncle's siblings
                for child in current_siblings: #scans through all siblings
                    child_spouses = child["SPOUSE"]
                    if (child_spouses != "NA"):
                        for spouse in child_spouses:
                            spouse_family = family_dic[spouse]
                            for sp in current_sp:
                                if (family_dic[sp]["WIFE"] in spouse_family["FAM_CHILD"]):
                                    current_sp_family = family_dic[sp].values()
                                    anomaly_array.append("ANOMALY: FAMILY: US20: {}: Person {} should not marry person {}".format(family_dic[sp]["HUSB_LINE"], family_dic[sp]["HUSB"], family_dic[sp]["WIFE"]))
                                    return False
                                elif(family_dic[sp]["HUSB"] in spouse_family["FAM_CHILD"]):
                                    anomaly_array.append("ANOMALY: FAMILY: US20: {}: Person {} should not marry person {}".format(family_dic[sp]["WIFE_LINE"], family_dic[sp]["WIFE"], family_dic[sp]["HUSB"]))
                                    return False
    return True

# US 21:
def correct_gender():
     for family in family_dic.values():
        if "husband_object" in family:
            husband_sex=family["husband_object"]["SEX"]
            if(husband_sex != "M"):
                error_array.append("ERROR: FAMILY: US21: {}: {}: Is Husband and has Sex as Female".format(family["husband_object"]["SEX_LINE"], family["husband_object"]["INDI"] ))
        if "wife_object" in family:
            wife_sex=family["wife_object"]["SEX"]
            if(wife_sex != "F"):
                error_array.append("ERROR: FAMILY: US21: {}: {}: Is Wife and has Sex as Male".format(family["wife_object"]["SEX_LINE"], family["wife_object"]["INDI"] ))

#USID: 25
# This checks the unique
def unique_family_name_and_birth():
    for value in family_dic.values():
        li = {}

        if "children_objects" in value:
            for child in value["children_objects"]:
                temp = child["NAME"] + child["BIRT"]

                if temp in li:
                    anomaly_array.append(f"ANOMALY: INDIVIDUAL: US25: {child['INDI']}: {li[temp]}: Individuals share the same name {child['NAME']} and birth date {child['BIRT']} from family {value['FAM']}")
                else:          
                    li[temp]=child["INDI"]

                                                 
#User_Story_29: List all deceased individuals in a GEDCOM file
#Prints out a table with all the deceased people's information
def listDeceased():
    current_dic = {}
    print("User_Story_29: List all deceased individuals in a GEDCOM file")
    for value in individuals.values():
        if(str(value["DEAT"]) != "NA" and (value["ALIVE"])):
            anomaly_array.append(("ERROR: INDIVIDUAL: US29: {}: Person is alive but has Death Date {}").format(value["NAME"], value["DEAT"]))
            print(("ERROR: INDIVIDUAL: US29: Person {} is alive but has Death Date {}").format(value["NAME"], value["DEAT"]))
        elif(str(value["DEAT"]) == "NA" and (not value["ALIVE"])):
            anomaly_array.append(("ERROR: INDIVIDUAL: US29: {}: Person is dead but has no Death Date").format(value["DEAT"]))
            print(("ERROR: INDIVIDUAL: US29: {}: Person is dead but has no Death Date").format(value["INDI"]))
        elif(not value["ALIVE"]):
            current_dic[value["INDI"]] = value    
    #Use pretty table module to print out the results
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT"]
    printTable("US29: Deceased People Table", allFields, tagNames, current_dic)


#User_Story_30: List all living married people in a GEDCOM file
#Prints out a table with all the living married people's information
def listLivingMarried():
    current_dic = {}
    print("User_Story_30: List all living married people in a GEDCOM file")
    for value in individuals.values():
        if(value["ALIVE"] and value["SPOUSE"] != "NA"):
            current_dic[value["INDI"]] = value
        elif(not value["ALIVE"] and value["SPOUSE"] != "NA"):
            anomaly_array.append("ERROR: INDIVIDUAL: US30: {}: Deceased Person is married to Person {}".format(value["INDI"], "".join(value["SPOUSE"])))
            print("ERROR: INDIVIDUAL: US30: {}: Deceased Person is married to Person {}".format(value["INDI"], "".join(value["SPOUSE"])))
    #Use pretty table module to print out the results
    allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
    tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]
    printTable("US30: Living & Married People Table", allFields, tagNames, current_dic)

                                                 
#US 32: List multiple births
def multiple_birth():
    for value in family_dic.values():
        li={}
        if "children_objects" in value:
            for child in value["children_objects"]:
                temp = str(child["INDI_CHILD"]) + child["BIRT"]
                if temp in li:
                    anomaly_array.append("ANOMALY: FAMILY: US32: {}: The two or more individuals were born at the same time in a family {}".format(value["FAM_LINE"], value["FAM"]))
                else:          
                    li[temp]=child["INDI"]                                                 
   
# US04 - Marriage Before Divorce

def is_marriage_after_divorce():
    # Iterating through all individuals
    for currentIndividual in individuals.values():
        # Ignoring all individuals who weren't ever married
        if(currentIndividual['SPOUSE'] != 'NA'):
            # Iterating through all the families they were related to
            for currentFamily in currentIndividual['SPOUSE']:
                for checkingFamily in family_dic.values():
                    if(checkingFamily['FAM'] == currentFamily):
                        # Ignoring all the marriages without a divorce
                        if(checkingFamily['DIV'] != 'NA'):
                            # Checking if a divorce date is before a marriage date
                            if(checkingFamily['MARR'] > checkingFamily['DIV']):
                                anomaly_array.append("ANOMALY: INDIVIDUAL: US04: {}: {}: Marriage Before Divorce - Marriage Date {} - Divorce Date {}".format(checkingFamily["MARR_LINE"], currentIndividual['INDI'], checkingFamily['MARR'], checkingFamily['DIV']))

# US05 - Marriage Before Death

def is_marriage_after_death():
    # Iterating through all individuals
    for currentIndividual in individuals.values():
        # Ignoring all individuals who weren't ever married
        if(currentIndividual['SPOUSE'] != 'NA'):
            # Iterating through all the families they were related to
            for currentFamily in currentIndividual['SPOUSE']:
                for checkingFamily in family_dic.values():
                    if(checkingFamily['FAM'] == currentFamily):
                        if(checkingFamily['MARR'] != 'NA'):
                            if(checkingFamily['MARR'] > currentIndividual['DEAT']):
                                anomaly_array.append("ANOMALY: INDIVIDUAL: US05: {}: {}: Marriage Before Death - Marriage Date {} - Death Date {}".format(checkingFamily["MARR_LINE"], currentIndividual['INDI'], checkingFamily['MARR'], currentIndividual['DEAT']))

# US34 List large age difference

def large_age_diff():
    
    for value in family_dic.values():
    #for family_id in family_dic:
        family= value["FAM"]
        if "husband_object" in family_dic[family]:
            husband=family_dic[family]["husband_object"]
            hage = int(husband["AGE"])
        if "wife_object" in family_dic[family]:
            wife=family_dic[family]["wife_object"]
            wage = int(wife["AGE"])
            agediff = hage/wage
            if agediff>=2 or agediff<=0.5:
                anomaly_array.append("ANOMALY: FAMILY: US34: {}: Family with unique id: {} has a large spouse age difference".format(value["FAM_LINE"], value["FAM"]))


#US 42
def validate_date():
    for value in individuals.values():
        if (value["BIRT"] != "NA"):
            birth = value["BIRT"]
            try:
                datetime.strptime(birth, '%Y-%m-%d')
            except ValueError:
                error_array.append("ERROR: INDIVIDUAL: US42: {}: Individual {} does not have valid Birth Date {}".format(value["BIRT_LINE"], value["INDI"], value["BIRT"]))
            
        if (value["DEAT"] != "NA"):
            death = value["DEAT"]
            try:
                datetime.strptime(death, '%Y-%m-%d')
            except ValueError:
                error_array.append("ERROR: INDIVIDUAL: US42: {}: Individual {} does not have valid Death Date {}".format(value["DEAT_LINE"], value["INDI"], value["DEAT"]))
                
    for value in family_dic.values():
        if (value["MARR"] != "NA"):
            marr = value["MARR"]
            try:
                datetime.strptime(marr, '%Y-%m-%d')
            except ValueError:
                error_array.append("ERROR: FAMILY: US42: {}: Famliy {} does not have valid Marriage Date {}".format(value["MARR_LINE"], value["FAM"], value["MARR"]))
                
        if (value["DIV"] != "NA"):
            div = value["DIV"]
            try:
                datetime.strptime(div, '%Y-%m-%d')
            except ValueError:
                error_array.append("ERROR: FAMILY: US42: {}: Famliy {} does not have valid Divorce Date {}".format(value["DIV_LINE"], value["FAM"], value["DIV"]))
        


# Prints out a table of dictionary data with the passed-in arguments
# Parameters:
# fields: a list of fields for the table
# tag_names: tag names used to access each data field
# dictionary: a dictionary filled with data
def printTable(table_name, fields, tag_names, dictionary):
    print(table_name)
    table = PrettyTable()
    table.field_names = fields
    for element in dictionary.values():    
        count = 1
        row_data = "" #string uses to store each tag within the current element
        for name in tag_names:
            if (count < int(len(tag_names))): #not the last element
                if (isinstance(element[name], list)): #current element is an array
                    row_data += (",".join(element[name]) + "? ")
                else: #current element is not an array
                    row_data += (str(element[name]) + "? ")
            elif (count == int(len(tag_names))):
                if (isinstance(element[name], list)): #current element is an array
                    row_data += (",".join(element[name]))
                else: #current element is not an array
                    row_data += (str(element[name]))
                break
            count+= 1
        table.add_row(row_data.split('?'))
    # Stores outputs to a text file
    storeResults(table_name, table.get_string())
    print(table)

def check_parents_not_too_old():
    """ US12: Mother should be less than 60 years older than her children and father should be less than 80 years older than his children """

    for family in family_dic.values():
        husband_flag = False
        wife_flag = False

        if "husband_object" in family and family["husband_object"] != 'NA':
            husband_age = family["husband_object"]["AGE"]
            husband_flag=True

        if "wife_object" in family and family["wife_object"] != 'NA':
            wife_age = family["wife_object"]["AGE"]
            wife_flag = True

        if "children_objects" in family and family["children_objects"] != 'NA':
            for child in family["children_objects"]:
                child_age = child["AGE"]
                husband_to_child = int(husband_age) - int(child_age)
                wife_to_child = int(wife_age) - int(child_age)
                
                if husband_flag and husband_to_child >= 80:
                    error_array.append(f'ERROR: INDIVIDUAL: US12: {family["husband_object"]["INDI_LINE"]}: {family["FAM"]}: Father is {husband_to_child} older than the child {child["INDI"]}.')

                if wife_flag and wife_to_child >= 60:
                     error_array.append(f'ERROR: FAMILY: US12: {family["wife_object"]["AGE"]}: {family["FAM"]}: Wife is {wife_to_child} older than the child {child["INDI"]}.')

def check_sibling_spacing():
    """ US13: Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day) """

    for family_id in family_dic:
        family = family_dic[family_id]

        if (len(family["FAM_CHILD"]) > 0) and family["FAM_CHILD"] != "NA":
            for child in family["FAM_CHILD"]:
                siblings = get_individual_siblings(child, False, True)
                child_object = individuals[child]

                for sibling in siblings:
                    if sibling != child:
                        sibling_object = individuals[sibling]
                        days = determine_days(child_object["BIRT"], sibling_object["BIRT"])
                        days = abs(days)

                        if 2 < days < (8 * 30):
                            error_array.append(f'ERROR: INDIVIDUAL: US13: {child_object["INDI_LINE"]}: Child {child} is born within 8 months and more than 2 days of sibling')



def get_individual_siblings(_id, include_husb, include_wife):
    individual = individuals[_id]
    siblings = []

    if "INDI_CHILD" in individual and individual["INDI_CHILD"] != "NA":
        for family_id in individual["INDI_CHILD"]:
            family = family_dic[family_id]

            if "FAM_CHILD" in family and family["FAM_CHILD"] != "NA":
                siblings.extend(family["FAM_CHILD"])

            if include_husb:
                if "husband_object" in family and family["husband_object"] != "NA":
                    siblings.extend(get_all_children(family["husband_object"]))

            if include_wife:
                if "wife_object" in family and family["wife_object"] != "NA":
                    siblings.extend(get_all_children(family["wife_object"]))

    siblings = list(set(siblings))

    return siblings  

def get_all_children(individual_object):
    spouses = individual_object["SPOUSE"]
    children = []

    if spouses != 'NA':
        for spouse_family_id in spouses:
            individual_family = family_dic[spouse_family_id]

            if (len(individual_family["FAM_CHILD"]) > 0) and individual_family["FAM_CHILD"] != "NA":
                children.extend(individual_family["FAM_CHILD"])

    return children

def check_sibling_marriage():

    #user story 18
    for individual_id in individuals:
        individual = individuals[individual_id]
        if "SPOUSE" in individual and individual["SPOUSE"] != "NA":
            siblings = get_individual_siblings(individual_id, True, True)
            for spouse_family_id in individual["SPOUSE"]:
                spouse_family = family_dic[spouse_family_id]
                spouse_id = None
                if "WIFE" in spouse_family and spouse_family["WIFE"] != "NA":
                    if spouse_family["WIFE"] != individual_id:
                        spouse_id = spouse_family["WIFE"]
                if "HUSB" in spouse_family and spouse_family["HUSB"] != "NA":
                    if spouse_family["HUSB"] != individual_id:
                        spouse_id = spouse_family["HUSB"]
                if spouse_id is not None and spouse_id in siblings:
                    anomaly_array.append("ANOMALY: INDIVIDUAL: US18: {}: {}: Individual married to sibling {}"                                         .format(individual["INDI_LINE"], individual_id, spouse_id))

def check_cousins_marriage():
    
    #user story 19
    for individual_id in individuals:
        individual = individuals[individual_id]
        if "SPOUSE" in individual and individual["SPOUSE"] != "NA":
            if "INDI_CHILD" in individual and individual["INDI_CHILD"] != "NA":
                cousins = []
                for child_in_family in individual["INDI_CHILD"]:
                    family = family_dic[child_in_family]
                    parent_siblings = []
                    if "HUSB" in family and family["HUSB"] != "NA":
                        parent_siblings.extend(get_individual_siblings(family["HUSB"], True, True))
                    if "WIFE" in family and family["WIFE"] != "NA":
                        parent_siblings.extend(get_individual_siblings(family["WIFE"], True, True))
                    for parent_sibling in parent_siblings:
                        cousins.extend(get_all_children(individuals[parent_sibling]))
                for spouse_family_id in individual["SPOUSE"]:
                    spouse_family = family_dic[spouse_family_id]
                    spouse_id = None
                    if "WIFE" in spouse_family and spouse_family["WIFE"] != "NA":
                        if spouse_family["WIFE"] != individual_id:
                            spouse_id = spouse_family["WIFE"]
                    if "HUSB" in spouse_family and spouse_family["HUSB"] != "NA":
                        if spouse_family["HUSB"] != individual_id:
                            spouse_id = spouse_family["HUSB"]
                    if spouse_id is not None and spouse_id in cousins:
                        anomaly_array.append("ANOMALY: INDIVIDUAL: US19: {}: {}: Individual married to cousin {}".format(individual["INDI_LINE"], individual_id, spouse_id))


def list_upcoming_bday():
    """ US38: List all living people in a GEDCOM file whose birthdays occur in the next 30 days """

    today_month = int(datetime.today().strftime("%m"))
    today_date = int(datetime.today().strftime("%d"))
    
    current_dic = {}
    bday_count = 0
    result = True
    
    for value in individuals.values():
        if (value["BIRT"] == 'NA'):
            error_array.append(f'ERROR: INDIVIDUAL: US38: {value["BIRT_LINE"]}: Person {value["BIRT"]} does not have birthday!')
            result = False
        else:
            current_birt = value["BIRT"]
            current_month = int(current_birt.split("-")[1])
            current_date = int(current_birt.split("-")[2])
            day_difference = (current_month - today_month)* 30 + (current_date- today_date)

            if (day_difference > 0 and day_difference <= 30):
                current_dic[value["INDI"]] = value
                bday_count += 1

    if bday_count > 0:
        allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
        tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]

        printTable("US38 List Upcoming Birthdays Table", allFields, tagNames, current_dic)
        
    return result

def list_upcoming_anni():
    """ US39: List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days """

    today_month = int(datetime.today().strftime("%m"))
    today_date = int(datetime.today().strftime("%d"))
    current_dic = {}
    marr_count = 0
    result = True

    for value in family_dic.values():
        if (value["MARR"] == 'NA'):
            error_array.append(f'ERROR: FAMILY: US39: {value["FAM_LINE"]}: Family {value["FAM"]} does not have married date!')
            result = False
        else:
            current_marr = value["MARR"]
            current_month = int(current_marr.split("-")[1])
            current_date = int(current_marr.split("-")[2])
            day_difference = (current_month - today_month) * 30 + (current_date - today_date)

            if (day_difference > 0 and day_difference <= 30):
                current_dic[value["FAM"]] = value
                marr_count += 1

    if marr_count > 0:
        allFields = ["ID", "Married", "Husband ID", "Husband Name", "Wife ID", "Wife Name"]
        tagNames = ["FAM", "MARR", "HUSB", "HUSB_NAME", "WIFE", "WIFE_NAME"]

        printTable("US39: List Upcoming Anniversaries Table", allFields, tagNames, current_dic)
        
    return result

def check_multiple_births():
    """ US14: No more than five siblings should be born at the same time """

    for family_id in family_dic:
        family = family_dic[family_id]

        if "FAM_CHILD" in family and family["FAM_CHILD"] != 'NA' and len(family["FAM_CHILD"]) > 0:
            random_child = family["FAM_CHILD"][0]

            siblings = get_individual_siblings(random_child, False, False)

            if len(siblings) < 5:
                continue

            birthdates = {}

            for sibling_id in siblings:
                individual = individuals[sibling_id]

                if individual is not None and individual != 'NA':
                    if "BIRT" in individual and individual["BIRT"] != 'NA':
                        if individual["BIRT"] in birthdates:
                            count = birthdates[individual["BIRT"]]
                            count += 1
                            birthdates[individual["BIRT"]] = count
                        else:
                            birthdates[individual["BIRT"]] = 1

            result = {k:v for (k,v) in birthdates.items() if v > 5}

            if len(result) > 0:
                anomaly_array.append(f'ANOMALY: FAMILY: US14: {family["FAM_LINE"]}: {family_id}: Family has more than 5 siblings with same birthdate')

def unique_family_by_spouses():
    """ US24: No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file """

    fams = []

    for family in family_dic.values():
        fam = {}
        compare = False
        
        if "husband_object" in family and family["husband_object"] != 'NA':
            fam["HUSB"] = family["husband_object"]["NAME"]
            compare = True

        if "wife_object" in family and family["wife_object"] != 'NA':
            fam["WIFE"] = family["wife_object"]["NAME"]
            compare = True

        if "MARR" in family and family["MARR"] != 'NA':
            fam["MARR"] = family["MARR"]
            compare = True

        if compare:
            if fam in fams:
                anomaly_array.append(f'ANOMALY: FAMILY: US24: {family["FAM_LINE"]}: {family["FAM"]}: Family contains same husband, wife and marriage date as another family')
            else:
                fams.append(fam)

def listLivingSingle():
    """ US31: List all living married people in a GEDCOM file """

    current_dic = {}
    single_count = 0
    result = True

    for value in individuals.values():
        if (value["AGE"] != "NA" and int(value["AGE"]) > 30 and value["ALIVE"] == True and value["SPOUSE"] == "NA"):
            if (value["BIRT"] == "NA"):
                error_array.append(f'ERROR: INDIVIDUAL: US31: {value["INDI_LINE"]}: Single Person {value["INDI"]} does not have birthday!')
                result = False
            else:
                current_dic[value["INDI"]] = value
                single_count += 1

    if single_count > 0:
        allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
        tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]

        printTable("US31: Unmarried people over 30", allFields, tagNames, current_dic)

    return result

def listAllOrphand():
    """ US33: List all multiple births in a GEDCOM file """

    current_dic = {}
    orphand_count = 0
    result = True

    for person in individuals.values():
        if (person["AGE"] == "NA"):
            error_array.append("ERROR: INDIVIDUAL: US33: {}: Orphaned child {} does not have age!".format(person["INDI_LINE"], person["INDI"]))
            result = False

        elif (int(person["AGE"]) < 18 and person["ALIVE"] == True):
            famID = person["INDI_CHILD"]

            if (isinstance(famID, list) == True):
                famID = "".join(famID)
            else:
                famID = str(famID)

            if (famID != "NA"):
                if (famID in family_dic.keys()):
                    currentFamily = family_dic[famID]
                    
                    current_husb = str(currentFamily["HUSB"])
                    current_wife = str(currentFamily["WIFE"])
                    
                    if (individuals[current_husb]["ALIVE"] == False and individuals[current_wife]["ALIVE"] == False):
                        current_dic[person["INDI"]] = person
                        orphand_count += 1
                else:
                    error_array.append(f'ERROR: INDIVIDUAL: US33: {person["INDI_LINE"]}: Orphaned child {person["INDI"]} does not belong to a family!')
                    result = False  
            else:
                error_array.append(f'ERROR: INDIVIDUAL: US33: {person["INDI_LINE"]}: Orphaned child {person["INDI"]} does not have a family ID!')
                result = False

    if orphand_count > 0:
        allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
        tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]

        printTable("US33: Orphaned Children", allFields, tagNames, current_dic)

    return result
    
# US 22: Unique IDs -> All individual IDs should be unique and all family IDs should be unique
def unique_indi_and_family(value, flag, line_num):
    if flag=="INDI":
        if value in ui:
            error_array.append("ERROR: INDIVIDUAL: US22: {}: {}: Individuals have the same ID".format(line_num, value))
            return False
        else:
            ui.append(value)
            return True
    else:       
        if value in uf:
            error_array.append("ERROR: FAMILY: US22: {}: {}: Two families share the same ID ".format(line_num, value))
            return False
        else:
            uf.append(value)
            return True

#US27 - Include Individual Ages in the INDIVIDUALS dictionary

def calculateAge(birthDate): 
    today = date.today() 
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
    return age 


def include_individual_ages():
    for currentIndividual in individuals.values():
        if(currentIndividual['DEAT'] == 'NA'):
            newArr = currentIndividual['BIRT'].split('-')
            age = calculateAge(date(int(newArr[0]), int(newArr[1]), int(newArr[2])))
            currentIndividual['AGE'] = age
        else:
            deathDate = currentIndividual['DEAT'].split('-')
            birthDate = currentIndividual['BIRT'].split('-')
            biggerNumber = calculateAge(date(int(birthDate[0]), int(birthDate[1]), int(birthDate[2])))
            smallerNumber = calculateAge(date(int(deathDate[0]), int(deathDate[1]), int(deathDate[2])))
            finalAge = biggerNumber - smallerNumber
            currentIndividual['AGE'] = finalAge
                          
#USID: 26
def check_corresponding_entries():
    for family_id in family_dic:
        family = family_dic[family_id]
        if "HUSB" in family and family["HUSB"] != "NA":
            husband_object = family["husband_object"]
            if husband_object != "NA" and family_id not in husband_object["SPOUSE"]:
                error_array.append("ERROR: FAMILY: US26: {}: {}: Husband id does not match with family id in individuals spouse entry".format(family["FAM_LINE"], family["HUSB"]))
        if "WIFE" in family and family["WIFE"] != "NA":
            wife_object = family["wife_object"]
            if wife_object != "NA" and family_id not in wife_object["SPOUSE"]:
                error_array.append("ERROR: FAMILY: US26: {}: {}: Wife id does not match with family id in individuals spouse entry".format(family["FAM_LINE"], family["WIFE"]))
        if "children_objects" in family and family["children_objects"] != "NA":
            for child_object in family["children_objects"]:
                if child_object != "NA" and family_id not in child_object["INDI_CHILD"]:
                    error_array.append("ERROR: FAMILY: US26: {}: {}: Child id does not match with family id in individuals spouse entry".format(family["FAM_LINE"], child_object["INDI"]))

#US28 List siblings in families by decreasing age, i.e. oldest siblings first
def listSiblingsByAge():
    error_count = 0
    print("US28: List siblings by decreasing age")
    file = open("cs555_sprint_outputs.txt", "a")
    file.write("US28: List siblings by decreasing age" + "\n")
    file.close()
    for fam in family_dic.values():
        currentSiblings = fam["FAM_CHILD"]
        sibling_count = 1
        if (currentSiblings != "NA"):
            current_dic = {}
            for sibling in currentSiblings:
                siblingAge = individuals[sibling]["AGE"]
                if (siblingAge == "NA"): #one of the siblings does not have age
                    error_array.append(("ERROR: FAMILY: US28: {}: Child {} has no age").format(individuals[sibling]["INDI_LINE"], sibling))
                    sibling_count = 0
                    error_count += 1
                    break;
                if int(siblingAge) in current_dic:
                    sibling_list = current_dic[int(siblingAge)]
                    sibling_list.append(sibling)
                    current_dic[int(siblingAge)] = sibling_list
                else:
                    sibling_list = [sibling]
                    current_dic[int(siblingAge)] = sibling_list
            if (sibling_count == 1):
                temp_dic = sorted(current_dic.keys(), reverse=True)
                resultList = []
                print("+-----Family " + str(fam["FAM"]) + "-----+")
                file = open("cs555_sprint_outputs.txt", "a")
                file.write("+-----Family " + str(fam["FAM"]) + "-----+" + "\n")
                for childList in temp_dic:
                    for child in current_dic[childList]:
                        resultList.append(str(child))
                        print("Individual:" + str(child) + ", Age:" + str(childList) + " ")
                        file.write("Individual:" + str(child) + ", Age:" + str(childList) + " \n")
#                 print("\n")
#                 file.write("\n")
                file.close()
        else: #no children in the family
            anomaly_array.append("ANOMALY: FAMILY: US28: {}: Family {} has no children".format(fam["FAM_LINE"], fam["FAM"]))
            error_count += 1
    print("\n")
    file = open("cs555_sprint_outputs.txt", "a")
    file.write("+-----End of US28-----+\n\n")
    file.close()
    return error_count

#US 35 List recent births
def list_recent_births():
    current_dic = {}
    bday_count = 0
    result = True
    
    for value in individuals.values():
        if (value["BIRT"] == 'NA'):
            error_array.append("ERROR: INDIVIDUAL: US35: {}: Person {} does not have birthday!".format(value["BIRT_LINE"], value["BIRT"]))
            result = False
        else:
            day_difference = determine_days(value["BIRT"], None)
            if (day_difference > 0 and day_difference <= 30):
                current_dic[value["INDI"]] = value
                bday_count += 1

    if bday_count > 0:
        #Use pretty table module to print out the results
        allFields = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Spouse"]
        tagNames = ["INDI", "NAME", "SEX", "BIRT", "AGE", "ALIVE", "DEAT", "SPOUSE"]
        printTable("US35 List Recent Births Table", allFields, tagNames, current_dic)   
    return result
        

def printTable(table_name, fields, tag_names, dictionary):
    """ Print table for US38 and US39 """

    print(table_name)

    table = PrettyTable()
    table.field_names = fields

    for element in dictionary.values():    
        count = 1
        row_data = ""

        for name in tag_names:
            if (count < int(len(tag_names))):
                if (isinstance(element[name], list)):
                    row_data += (",".join(element[name]) + "? ")
                else: #current element is not an array
                    row_data += (str(element[name]) + "? ")
            elif (count == int(len(tag_names))):
                if (isinstance(element[name], list)):
                    row_data += (",".join(element[name]))
                else:
                    row_data += (str(element[name]))
                break

            count+= 1
        table.add_row(row_data.split('?'))
    
    storeResults(table_name, table.get_string())
    print(table)

# Stores all Project outputs into a single text file
# Parameters:
# result_name: name that will appear 
def storeResults(result_name, outputs):
    file = open("ssw555_sprint_outputs.txt", "a")
    file.write(result_name + "\n")
    file.write(outputs + "\n\n")
    file.close()

def find_name(arr, _id):
    for indi in arr:
        if _id == indi["INDI"]:
            return indi["NAME"]

# Reads the input GEDCOM file line by line and store the data into the dictionary
def read_in(file):
    doc={"INDI":[], "FAM":[]}
    dic={}
    flag=False #indicates whether the correct tag has appeared before DATE tag
    with open(file) as f:
        all_lines=f.readlines()
        line_num = 1; #line number of each 
        for line, next_line in zip(all_lines, all_lines[1:]):
            current_arr=line.strip().split(" ")
            next_arr=next_line.strip().split(" ")
            #if the current tag is individual
            if len(current_arr)==3 and current_arr[0]=='0' and current_arr[2]== "INDI":
                #inserts individual's ID into the dictionary
                dic, current_tag=create_dic_entry(current_arr, "INDI") 
                #inserts line number
                dic["INDI_LINE"] = line_num
            #if the current tag is family
            elif len(current_arr)==3 and current_arr[0]=='0' and current_arr[2]=="FAM": 
                dic, current_tag=create_dic_entry(current_arr, "FAM")
                #inserts line number
                dic["FAM_LINE"] = line_num
            #if the current tag is date
            elif current_arr[1]=="DATE" and flag:
                flag=False
                date_arr = current_arr[2:] #extracts the date argument from the line
                dic[tmp]= convert_date(date_arr) #converts the date into correct format
            #determines if the tag level is correct
            elif current_arr[0]=='1' and current_arr[1] in supported_tag:
            #"NAME", "SEX", "BIRT", "DEAT","FAMC","FAMS","MARR", "DIV","HUSB","WIFE","CHIL"
                if (isDateParent(current_arr)): #determines whether the current tag is parent of DATE tag
                    tmp=current_arr[1] #extracts the tag name
                    flag=True
                    #inserts line number
                    dic[tmp + "_LINE"] = line_num
                else: 
                    #current tag is not the parent tag of DATE tag
                    if current_arr[1] == "HUSB":
                        dic["HUSB_NAME"]=find_name(doc["INDI"], current_arr[2])
                        #inserts line number
                        dic["HUSB_LINE"] = line_num
                    if current_arr[1] == "WIFE":
                        dic["WIFE_NAME"]=find_name(doc["INDI"], current_arr[2])
                        #inserts line number
                        dic["WIFE_LINE"] = line_num
                    if current_arr[1] == 'CHIL':
                        #INDI_CHILD indicates all the children within a family
                        children = dic["FAM_CHILD"] if "FAM_CHILD" in dic else []
                        children.append(current_arr[2])
                        dic["FAM_CHILD"] = children
                        #inserts line number
                        dic["CHIL_LINE_" + current_arr[2]] = line_num
                    if current_arr[1] == 'FAMC' or current_arr[1] == 'FAMS':
                        child = dic["INDI_CHILD"] if "INDI_CHILD" in dic else []
                        spouse = dic["SPOUSE"] if "SPOUSE" in dic else []
                        child.append(current_arr[2]) if current_arr[1] == 'FAMC' else spouse.append(current_arr[2])
                        dic['INDI_CHILD'] = child #FAM_CHILD indicates which family this individual belongs to
                        dic['SPOUSE'] = spouse
                        #inserts line number
                        dic[current_arr[1] + "_LINE"] = line_num
                    else: #other type of tag
                        dic[current_arr[1]]=' '.join(current_arr[2:])
                        #inserts line number
                        dic[current_arr[1] + "_LINE"] = line_num
            #TRLR ==> end of the GEDCOM file
            if (len(next_arr)==3 and next_arr[0]=='0' and next_arr[2] in def_tag) or next_arr[1]=="TRLR":
                if dic: #if the dic exists or not
                    if current_tag == 'INDI': #under individual tag?
                        if 'DEAT' in dic:
                            age = determine_age(dic['BIRT'], dic['DEAT'])
                            alive = False
                        else:
                            age = determine_age(dic['BIRT'], None)
                            alive = True
                            dic['DEAT'] = "NA"
                        dic["AGE"] = str(age)
                        dic['ALIVE']= alive
                        if not dic["SPOUSE"]:
                            dic["SPOUSE"] = "NA"
                        elif not dic["INDI_CHILD"]:
                            dic["INDI_CHILD"] = "NA"
                    if current_tag == 'FAM':
                        add_missing_entries(dic)
                    doc[current_tag].append(dic) 
            line_num += 1 #increments the line counter by 1
        return doc                  

document = read_in("./test.ged")

for family in document["FAM"]:
    husband = family["HUSB"] if "HUSB" in family else []
        
indi_table = PrettyTable()
indi_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
fam_table = PrettyTable()
fam_table.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]


for individual in document["INDI"]:
    indi_id = individual["INDI"].strip('@')
    indi_table.add_row([indi_id, individual["NAME"], individual["SEX"], individual["BIRT"], individual["AGE"], 
                       individual["ALIVE"], individual["DEAT"], (",".join(individual["INDI_CHILD"])), (",".join(individual["SPOUSE"]))])
    
for family in document["FAM"]:
    fam_id = family["FAM"].strip('@')
    fam_table.add_row([fam_id, family["MARR"], family["DIV"], family["HUSB"].strip('@'), family["HUSB_NAME"], family["WIFE"].strip('@'), family["WIFE_NAME"], ({",".join(family["FAM_CHILD"])})])
    

print(indi_table)
print(fam_table)


