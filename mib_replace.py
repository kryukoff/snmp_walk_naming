import pandas as pd
import requests

#walk_file - exported from ireasoning snmp_walk to XML -> CSV -> XLSX
walk_file = "myxls.xlsx"

#vendor - oriented mib file
snmp_file = ""
#replace with vendor mib xlsx file

#standard ups mib
ups_mib_file = "UPS-MIB.xlsx"

#standard general purpouse mib
standard_mib_file = "SNMPv2-MIB.xlsx"

#output modified file
output_file = 'modified2.xlsx'

walk_df = pd.read_excel(walk_file)
mib_df = pd.read_excel(snmp_file)
ups_mib_df = pd.read_excel(ups_mib_file) 
standard_mib_df = pd.read_excel(standard_mib_file) 


# Remove first period from each value in "name" column
walk_df['name'] = walk_df['name'].str.replace('^\.', '', regex=True)

# Remove everything after the last period in each value
walk_df['name'] = walk_df['name'].str.replace('\.[0-9]*$', '', regex=True)


replacements = 0
#dict from OID file, matching OID and description
name_to_full_name_map = dict(zip(mib_df['OID'], mib_df['Full Name']))
for i, name in enumerate(walk_df['name']):
    if name in name_to_full_name_map:
        walk_df.at[i, 'name'] = name_to_full_name_map[name]
        replacements += 1
print("Number of replacements made from vendor mib: ", replacements)


replacements = 0
#dict from OID file, matching OID and description
name_to_full_name_map = dict(zip(ups_mib_df['OBJECT_IDENTIFIER'], ups_mib_df['OBJECT_DESCRIPTION']))
for i, name in enumerate(walk_df['name']):
    if name in name_to_full_name_map:
        walk_df.at[i, 'name'] = name_to_full_name_map[name]
        replacements += 1
print("Number of replacements made from ups mib: ", replacements)


replacements = 0
#dict from OID file, matching OID and description\
name_to_full_name_map = dict(zip(standard_mib_df['OBJECT_IDENTIFIER'], standard_mib_df['OBJECT_DESCRIPTION']))
for i, name in enumerate(walk_df['name']):
    if name in name_to_full_name_map:
        walk_df.at[i, 'name'] = name_to_full_name_map[name]
        replacements += 1
print("Number of replacements made from standard mib: ", replacements)


#fill the rest of oids from oid-info.com
replacements = 0
for index, row in walk_df.iterrows():
    if row['name'] in row['oid']:
        try:
            url = 'http://oid-info.com/get/'
            oid = str(row['name'])
            url2 = url+oid
            print('parsing...')
            r = requests.get(url2)
            b = r.text.replace('<br>', '').replace('<br/>', '')
            b = b.split("DESCRIPTION")[1].split('</code>')[0]
            walk_df.at[index, 'name'] = b
            replacements += 1
            #print(type(b))
        except:
            print("didnt come out")
        
print("Number of replacements made from oid-info: ", replacements)
    
        

walk_df.to_excel(output_file, index=False)
