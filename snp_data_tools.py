import re
import magic
import os
from zipfile import ZipFile
import gzip
'''import pyliftover
import pysam'''

genome_build_coords = "./genome_build_coords.txt"


class SNPZipFile():
    def __init__(self, zipped_file):
        self.zipped_file = zipped_file

    def unzip_file(self):
        os.mkdir("./temp")
        with ZipFile(self.zipped_file, 'r') as zip:
            zip.extractall("./temp")

    def file_type(self):
        dir = "./temp"
        with magic.Magic() as m:
            for filename in os.listdir(dir):
                file = dir+filename
                filetype = m.id_filename(file)
                if "ASCII" or "RSID" not in filetype:
                    if "PDF" in filetype:
                        print(file, "PDF")
                    elif "gzip" in filetype:
                        print(file, "gzip")
                    elif "Excel" in filetype:
                        print(file, "Excel")
                    elif "Zip" in filetype:
                        with ZipFile(file, 'r') as zip:
                            zip.extractall()
                        print(file, "Zip")
                    else:
                        print(file, "unknown type")


class SNP():
    def __init__(self, rsid, chromosome, position, allele1, allele2):
        self.rsid = rsid
        self.chromosome = chromosome
        self.position = position
        self.allele1 = allele1
        self.allele2 = allele2

    def convert(self):
            row = self.strip()
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

    def make_snp_file(self):
        snps_array = []
        with open(self, 'r') as infile:
            snps_array = [SNP.convert(row)for row in infile if not (row.startswith("RSID") or row.startswith("#") or row.startswith("rsid"))]
            return SNPArray(snps_array)

    def change_genome_version(self):
        pass

    def to_VCF(self):
        pass


class GenomeVersion():
    def __init__(self, genome_build):
        self.genome_build = genome_build

    def get_genome_version_from_metadata(self):
        with open(self, 'r') as infile:
            # check for genome build in the first 25 lines
            for x in range(25):
                row = next(infile)
                result = re.search('(?<=build )(..)', row)
                if result is not None:
                    genome_build = result.group(1)
                    break
        return genome_build

    def get_genome_version_from_coordinates(self):
        with open(self, 'r') as infile:
            with open(genome_build_coords, 'r') as coords:
                row = next(infile)
                if not (row.startswith("RSID") or row.startswith("#") or row.startswith("rsid")):
                    snp = SNP.convert(row)
                    rsid = next(coords)
                    if snp.rsid == rsid[0]:
                        if snp.position == rsid[1]:
                            genome_build = "36"
                        elif snp.position == rsid[2]:
                            genome_build = "37"
                        elif snp.position == rsid[3]:
                            genome_build = "38"
                return genome_build
