import re
'''import magic
import os
import zipfile
import gzip'''


class zip_file():
    def __init__(self, phenotype):
        self.phenotype = phenotype

    pass


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


class SNPArray():
    def __init__(self, snps=[]):
        self.snps = snps
        # self.snps = snps
        # self.snp_file = snp_file

    def __getitem__(self, i):
        return self.snps[i]

    def __iter__(self):
        return self

    @staticmethod
    def make_snp_file(snp_file):
        snps_array = []
        with open(snp_file, 'r') as infile:
            snps_array = [SNP.convert(row)for row in infile if not (row.startswith("RSID") or row.startswith("#") or row.startswith("rsid"))]

            return SNPArray(snps_array)

    def __repr__(self):
        return "{}".format(self.snps)
