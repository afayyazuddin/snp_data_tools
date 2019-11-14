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
snp_coords = []

for file in os.listdir(directory):
    os.listdir(directory)
    if not file.startswith("."):
        with open(directory + "/" + file, 'r') as infile:
            coords = iter(infile.readlines())
            next(coords)
            while True:
                snp = next(coords)
                if not (snp.startswith("RSID") or snp.startswith("#") or snp.startswith("rsid") or not snp.strip()):
                    snp_row = SNP.convert(snp)
                    rsid = snp_row.rsid
                    if "rs" in rsid:
                        break
            if rsid not in snp_list:
                snp_list.append(rsid)
snp_list = ', '.join(['"{}"'.format(value) for value in snp_list])

connection = MySQLdb.connect(host='genome-mysql.cse.ucsc.edu', user='genome', password='')
c = connection.cursor()

for genome_build, table in genome_list:
    database_command = 'use {}'.format(genome_build)
    sql_command = 'select name,chrom,chromStart from {} where name in ({})'.format(table, snp_list)
    connection_command = "host='genome-mysql.cse.ucsc.edu', user='genome', password='', db='{}'".format(genome_build)
    c.execute(database_command)
    c.execute(sql_command)
    output = c.fetchall()
    snp_coords.append(output)
print(snp_coords)
connection.close()
