"""
    @author Jenish Kevadia

    Script reads the data from gedcom file and validates whether it's correct or not
"""

supported_tags = ['HEAD', 'TRLR', 'NOTE', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']
define_tags = ['INDI', 'FAM']
name_tag = 'NAME'
date_tag = 'DATE'
output = []

with open('test.ged', 'r') as file:
    lines = file.readlines()

    file.close()

for line in lines:
    level, tag, *args = line.split()
    valid = None

    output.append(f'--> {line}')

    if tag not in supported_tags:
        if args and args[0] in define_tags:
            valid = 'Y'
            out_line = f'<-- {level}|{args[0]}|{valid}|{tag}\n'
            output.append(out_line)
        elif level == '1' and tag == name_tag:
            valid = 'Y'
            out_line = f'<-- {level}|{tag}|{valid}|'+' '.join(args)+'\n'
            output.append(out_line)
        elif level == '2' and tag == date_tag:
            valid = 'Y'
            out_line = f'<-- {level}|{tag}|{valid}|'+' '.join(args)+'\n'
            output.append(out_line)
        else:
            valid = 'N'
            out_line = f'<-- {level}|{tag}|{valid}|'+' '.join(args)+'\n'
            output.append(out_line)
    else:
        valid = 'Y'
        out_line = f'<-- {level}|{tag}|{valid}|'+' '.join(args)+'\n'
        output.append(out_line)

with open('output.txt', 'w') as file:
    file.writelines(output)