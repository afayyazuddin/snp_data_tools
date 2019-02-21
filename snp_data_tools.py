import re
'''import magic
import os
import zipfile
import gzip'''


class zip_file():
    def __init__(self, phenotype):
        self.phenotype = phenotype

    pass


class snp_file():
    def __init__(self, genome_version):
        self.genome_version = genome_version


class SNP():
    def __init__(self, rsid, chromosome, position, allele1, allele2):

        self.rsid = rsid
        self.chromosome = chromosome
        self.position = position
        self.allele1 = allele1
        self.allele2 = allele2

    @staticmethod
    def convert(row):
        row = row.strip()
        splitrow = re.split('[, \t]', row)
        # splitrow=row.split(",")
        rsid = splitrow[0].strip('\"')
        chromosome = splitrow[1].strip('\"')
        position = splitrow[2].strip('\"')
        splitrow[3] = splitrow[3].strip('\"')
        if len(splitrow[3]) == 2:
            allele1 = splitrow[3][0]
            allele2 = splitrow[3][1]
        else:
            allele1 = splitrow[3]
            allele2 = splitrow[4]
        return SNP(rsid, chromosome, position, allele1, allele2)

    def __str__(self):
        return "{} at chromosome {} position {} with variants {} and {}".format(self.rsid, self.chromosome, self.position, self.allele1, self.allele2)

    def __repr__(self):
        return "SNP (rsid={}, chromosome={}, position={}, allele1={}, allele2={})".format(self.rsid, self.chromosome, self.position, self.allele1, self.allele2)
