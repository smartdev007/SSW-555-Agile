from datetime import datetime
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
                 anomaly_array.append(("ERROR: INDIVIDUAL: US02: {}: Person has marriage date {} before birth date {}").format(family["wife_object"]["INDI"], marriage_date, wife_birth_date))



def find_name(arr, _id):
    for indi in arr:
        if _id == indi["INDI"]:
            return indi["NAME"]

def read_in(file):
    doc = {"INDI": [], "FAM": []}
    dic = {}
    flag = False

    with open(file) as f:
        all_lines = f.readlines()
        for line, next_line in zip(all_lines, all_lines[1:]):
            current_arr = line.strip().split(" ")
            next_arr = next_line.strip().split(" ")
            
            if len(current_arr) == 3 and current_arr[0] == '0' and current_arr[2] == "INDI":
                current_tag = "INDI"
                dic = {}
                dic["INDI"] = current_arr[1]
            elif len(current_arr) == 3 and current_arr[0] == '0' and current_arr[2] == "FAM": 
                current_tag = "FAM"
                dic = {}
                dic["FAM"] = current_arr[1]
            elif (current_arr[1] == "DATE" and flag):
                flag = False
                date_arr = current_arr[2:]
                dic[tmp] = convert_date(date_arr)
            elif current_arr[0] == '1' and current_arr[1] in supported_tag:
                if (isDateParent(current_arr)):
                    tmp = current_arr[1]
                    flag = True
                else: 
                    if current_arr[1] == "HUSB":
                        husband = find_name(doc["INDI"], current_arr[2])
                        dic["HUSB_NAME"] = husband
                    if current_arr[1] == "WIFE":
                        husband = find_name(doc["INDI"], current_arr[2])
                        dic["WIFE_NAME"] = husband
                    if current_arr[1] == 'CHIL':
                        children = dic["FAM_CHILD"] if "FAM_CHILD" in dic else []
                        children.append(f"{current_arr[2].strip('@')}")
                        dic["FAM_CHILD"] = children
                    if current_arr[1] == 'FAMC' or current_arr[1] == 'FAMS':
                        child = dic["INDI_CHILD"] if "INDI_CHILD" in dic else []
                        spouse = dic["SPOUSE"] if "SPOUSE" in dic else []
                        if current_arr[1] == 'FAMC':
                            child.append(f"{current_arr[2].strip('@')}")
                        else:
                            spouse.append(f"{current_arr[2].strip('@')}")
                        dic['INDI_CHILD'] = child
                        dic['SPOUSE'] = spouse
                    else:
                        dic[current_arr[1]] = ' '.join(current_arr[2:])

            if (len(next_arr) == 3 and next_arr[0] =='0' and next_arr[2] in def_tag) or next_arr[1] == "TRLR":
                if dic:
                    if current_tag == 'INDI':
                        if 'DEAT' in dic:
                            age = determine_age(dic['BIRT'], dic['DEAT'])
                            alive = False
                        else:
                            age = determine_age(dic['BIRT'], None)
                            alive = True
                            dic['DEAT'] = 'NA'
                        dic["AGE"] = str(age)
                        dic['ALIVE'] = alive
                        
                        if not dic["SPOUSE"]:
                            dic["SPOUSE"] = ["NA"]
                        elif not dic["INDI_CHILD"]:
                            dic["INDI_CHILD"] = ["NA"]

                    if current_tag == 'FAM':
                        if "DIV" not in dic:
                            dic["DIV"] = ["NA"]
                        if "HUSB" not in dic:
                            dic["HUSB"] = ["NA"]
                        if "HUSB_NAME" not in dic:
                            dic["HUSB_NAME"] = ["NA"]
                        if "WIFE" not in dic:
                            dic["WIFE"] = ["NA"]
                        if "WIFE_NAME" not in dic:
                            dic["WIFE_NAME"] = ["NA"]
                        if "FAM_CHILD" not in dic:
                            dic["FAM_CHILD"] = ["NA"]
                        if "MARR" not in dic:
                            dic["MARR"] = ["NA"]   

                    doc[current_tag].append(dic)
                    
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
