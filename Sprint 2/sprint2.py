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

def determine_days(d1, d2):
    """ Determine difference between days for US08 and US09 """
    year1 = int(d1.split('-')[0])
    month1 = int(d1.split('-')[1])
    day1 = int(d1.split('-')[2])
    
    year2 = int(d2.split('-')[0])
    month2 = int(d2.split('-')[1])
    day2 = int(d2.split('-')[2])
    
    return (year2 - year1) * 365 + (month2 - month1) * 30 + day2- day1

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
