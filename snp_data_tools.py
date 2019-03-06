import re
'''import magic
import os
import zipfile
import gzip
import pyliftover
import pysam'''


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
            if len(splitrow) == 5:
                allele1 = splitrow[3]
                allele2 = splitrow[4]
            else:
                if len(splitrow[3]) == 2:
                    allele1 = splitrow[3][0]
                    allele2 = splitrow[3][1]
                else:
                    allele1 = splitrow[3][0]
                    allele2 = ""

            return SNP(rsid, chromosome, position, allele1, allele2)

    def __str__(self):
        return "{} at chromosome {} position {} with variants {} and {}".format(self.rsid, self.chromosome, self.position, self.allele1, self.allele2)

    def __repr__(self):
        return "SNP (rsid={}, chromosome={}, position={}, allele1={}, allele2={})".format(self.rsid, self.chromosome, self.position, self.allele1, self.allele2)


class SNPArray():
    def __init__(self, snps=[]):
        self.snps = snps
        # self.genome_version = genome_version

    # allow indexing of SNPArray object
    def __getitem__(self, i):
        return self.snps[i]

    def __iter__(self):
        return self

    def __repr__(self):
        return "{}".format(self.snps)

    @staticmethod
    def make_snp_file(snp_file):
        snps_array = []
        with open(snp_file, 'r') as infile:
            snps_array = [SNP.convert(row)for row in infile if not (row.startswith("RSID") or row.startswith("#") or row.startswith("rsid"))]
            return SNPArray(snps_array)

    def change_genome_version(self):
        pass

    def to_VCF(self):
        pass


class genome_version():
    def __init__(self, genome_build):
        self.genome_build = genome_build

    @staticmethod
    def get_genome_version(snp_file):
        with open(snp_file, 'r') as infile:
            # check for genome build in the first 25 lines
            for x in range(25):
                row = next(infile)
                result = re.search('(?<=build )(..)', row)
                if result is not None:
                    genome_build = result.group(1)
                    break
            if result is None:
                while result is None:
                    # rsids = [SNP.convert(next(infile))[0]for x in range(5)]
                    rsid = SNP.convert(next(infile))
                    # check rsid coordinates against coordinates for genome versions

        return genome_build
