import re
import argparse
import magic
import sys
import os
import csv
from zipfile import ZipFile
import xlrd
import gzip
import pyliftover
import pysam

with open("/Users/amir/Documents/Analysis/snp_data_tools/genome_build_coords.txt", 'r') as infile:
    coords = iter(infile.readlines())


'''def convert_zip():
        pass

    def convert_pdf():
        pass

    def convert_gzip():
        pass

    def convert_excel(self):
        workbook = xlrd.open_workbook(self)
        # workbook.sheet_names()
        first_sheet = workbook.sheet_by_index(0)
        with open(self, 'w') as outfile:
            for rownum in range(first_sheet.nrows):
                outfile.write(first_sheet.row_values(rownum))'''


# SNP class encodes the genome coordinates and alleles of each
# variant in the genotype file
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

    # allow indexing of SNPArray object
    def __getitem__(self, i):
        return self.snps[i]

    def __iter__(self):
        return self

    def __repr__(self):
        return "{}".format(self.snps)

    def extract_file_type(self):
        with magic.Magic() as m:
            # for filename in os.listdir(dir):
            #    file = dir+filename
            return m.id_filename(self)

    def get_genome_version_from_metadata(self):
        # check for genome build in the first 25 lines
        for x in range(25):
            row = self[x]
            result = re.search('(?<=build )(..)', row)
            if result is not None:
                genome_build = result.group(1)
                break
        return genome_build

    def get_genome_version_from_coordinates(self):
        match = False
        file = iter(self)
        while match is not True:
            row = next(file)
            if not (row.startswith("RSID") or row.startswith("#") or row.startswith("rsid")):
                snp = SNP.convert(row)
                rsid = next(coords)
                rsid = rsid.strip()
                rsid = rsid.split("\t")
                if snp.rsid == rsid[0]:
                    match = True
                    if snp.position == rsid[1]:
                        genome_build = "36"
                    elif snp.position == rsid[2]:
                        genome_build = "37"
                    elif snp.position == rsid[3]:
                        genome_build = "38"
                    return genome_build

    def change_genome_version(self):
        pass

    def to_VCF(self):
        pass

    '''def make_snp_file(self):
        snps_array = []
        if [row[0].startswith("#") for row in self]:
            genome_build = self.get_genome_version_from_metadata()
        else:
            genome_build = self.get_genome_version_from_coordinates()
        # put in if-else to direct it to convert coordinates if genome version is different from desired one
        snps_array = [SNP.convert(row)for row in self if not (row.startswith("RSID") or row.startswith("#") or row.startswith("rsid"))]
        for row in self:
            if not row.startswith("RSID") or row.startswith("#") or row.startswith("rsid"):
                snps_array =
        return SNPArray(snps_array)'''

    def convert_text(self, outdir):
        file_identifier = self.split("/")[-1].split("_")
        user = file_identifier[0]
        file = file_identifier[1]
        out_dir_file = outdir + "/" + user + "_" + file + ".txt"
        with open(self, 'r') as infile:
            with open(out_dir_file, 'w') as outfile:
                csv_writer = csv.writer(outfile, delimiter="\t")
                x = 1
                for row in infile:
                    if not (row.startswith("RSID") or row.startswith("#") or row.startswith("rsid")):
                        '''print(row)
                        x = x + 1
                        if x == 11:
                            break'''
                        SNP_row = SNP.convert(row)
                        csv_writer.writerow((SNP_row.rsid, SNP_row.chromosome, SNP_row.position, SNP_row.allele1 + SNP_row.allele2))
                        # convert SNP to row

            #filetype = infile.extract_file_type()
            #return filetype
            #return infile.make_snp_file()


if __name__ == "__main__":
    # args = parse_args(sys.argv[1:])
    parser = argparse.ArgumentParser(sys.argv[1:])
    # parser.add_argument("-f", "--files", help="filenames with type")
    parser.add_argument("-g", "--genome", help="reference genome build, \
    default = 37")
    parser.add_argument("-o", "--output", help="output directory")
    parser.add_argument("-i", "--input", help="input directory")
    # parser.add_argument("-f", "--format", help="output format \
    # default = vcf: VCF")
    arguments = parser.parse_args()
    print(arguments)
    for file in os.listdir(arguments.input):
        if os.path.isdir(file):
            pass
        elif file.startswith("."):
            pass
        else:
            file_name = arguments.input + "/" + file
            # print(file_name)
            if "text" in SNPArray.extract_file_type(file_name):
                SNPArray.convert_text(file_name, arguments.output)
                print("text")
            elif "PDF" in SNPArray.extract_file_type(file_name):
                print("PDF")
            elif "gzip" in SNPArray.extract_file_type(file_name):
                print(file, "gzip")
            elif "Excel" in SNPArray.extract_file_type(file_name):
                print(file, "Excel")
            elif "Zip" in SNPArray.extract_file_type(file_name):
                print(file, "zip")
            else:
                print(file, "unknown type")
                # with open(file, 'r'):
                #    SNPArray.make_snp_file(file)'''
