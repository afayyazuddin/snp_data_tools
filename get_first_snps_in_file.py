'''
script to find the first rsid from arrays to identify genome build
from coordinates
usage: "python get_first_snps_in_file.py name_of_directory"
'''
import os
import sys
from snp_data_tools import SNP

directory = sys.argv[1]
snp_list = []

for file in os.listdir(directory):
    os.listdir(directory)
    if not file.startswith("."):
        with open(directory + "/" + file, 'r') as infile:
            coords = iter(infile.readlines())
            next(coords)
            while True:
                try:
                    snp = next(coords)
                    if not (snp.startswith("RSID") or snp.startswith("#") or snp.startswith("rsid") or not snp.strip()):
                        snp_row = SNP.convert(snp)
                        rsid = snp_row.rsid
                        if "rs" in rsid:
                            break
                except StopIteration:
                    break
            if rsid not in snp_list:
                snp_list.append(rsid)
                print(snp_list)
print(*snp_list, sep='\n')
