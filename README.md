# snmp_walk_naming
Script to name SNMP_walk OIDs, thats description weren't identified / missed

On input an xlsx file with columns "name" and "oid"

Unidentified OIDs contains oid in both fields - "name" and "oid"

Script firstly tries to find OIDs in connected XLSX files
Then still unidentified oids tried to find online

#standard ups mib
ups_mib_file = "UPS-MIB.xlsx"

#standard general purpouse mib
standard_mib_file = "SNMPv2-MIB.xlsx"
