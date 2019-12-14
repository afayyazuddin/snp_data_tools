'''
script to find the first rsid from arrays to identify genome build
from coordinates
usage: "python get_first_snps_in_file.py name_of_directory"
'''
import os
import sys
import MySQLdb
from snp_data_tools import SNP

directory = sys.argv[1]
genome_list = [["hg18", "snp130"], ["hg19", "snp150"]]
snp_list = []
# snp_coords = []
snp_coords = {}

for file in os.listdir(directory):
    os.listdir(directory)
    if not file.startswith("."):
        with open(directory + "/" + file, 'r') as infile:
            coords = iter(infile.readlines())
            # next(coords)
            while True:
                snp = next(coords)
                if not (snp.startswith("RSID") or snp.startswith("#") or snp.startswith("rsid") or not snp.strip()):
                    snp_row = SNP.convert(snp)
                    rsid = snp_row.rsid
                    if "rs" in rsid:
                        break
            if rsid not in snp_list:
                snp_list.append(rsid)
                print(snp_list)

connection = MySQLdb.connect(host='genome-mysql.cse.ucsc.edu', user='genome', password='')
c = connection.cursor()

# get SNP coordinates from UCSC SNP database using mysql query
# output nested dictionary that contains snp coordinates for first snps
# arranged by genome_build
for genome_build, table in genome_list:
    coords_by_genome = {}
    for snp in snp_list:
        database_command = 'use {}'.format(genome_build)
        sql_command = 'select chrom,chromStart from {} where name in ("{}")'.format(table, snp)
        c.execute(database_command)
        c.execute(sql_command)
        output = c.fetchall()
        for row in output:
            output = (row[0], row[1])
        coords_by_genome[snp] = output
    snp_coords[genome_build] = coords_by_genome

print(snp_coords)
with open('genome_build_coords.txt', 'w') as outfile:
    outfile.write(str(snp_coords))
connection.close()
