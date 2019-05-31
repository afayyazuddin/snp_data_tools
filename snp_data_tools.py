import re
import argparse
import magic
import sys
import os
import multiprocessing as mp
import csv
from zipfile import ZipFile
import xlrd
import gzip
# from pyliftover import LiftOver
import time
# import pysam

start = time.time()
with open("/Users/amir/Documents/Analysis/snp_data_tools/genome_build_coords.txt", 'r') as infile:
    coords = iter(infile.readlines())


def write_file(self):
    with open(out_dir_file, 'w') as outfile:
        for row in self:
            csv_writer = csv.writer(outfile, delimiter="\t")
            csv_writer.writerows([row.split("\t")])


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
        # print(SNP(rsid, chromosome, position, allele1, allele2))
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

    def convert_text(self):
        SNP_row = SNP.convert(self)
        return (SNP_row.rsid + "\t" + SNP_row.chromosome + "\t" + SNP_row.position + "\t" + SNP_row.allele1 + SNP_row.allele2)

    def multiprocess_text(self):
        p = mp.Pool(arguments.threads)
        result = p.map(SNPArray.convert_text, [row for row in self if not (row.startswith("RSID") or row.startswith("#") or row.startswith("rsid") or not row.strip())])
        write_file(result)
        ''' ignore lines that are empty, are comments or are headers'''

    def text_file(self):
        with open(self, 'r') as infile:
            SNPArray.multiprocess_text(infile)

    def gzip_file(self):
        with gzip.open(self, 'r') as infile:
            all_data = infile.read().split()
            decoded_file = [row.decode("utf-8")for row in all_data]
            SNPArray.multiprocess_text(decoded_file)

    def zip_file(self):
        with ZipFile(self, 'r') as zip:
            name = zip.namelist()[0]
            print(name)
            decoded_file = zip.read(name).decode("utf-8")
            decoded_file = decoded_file.split("\n")
            decoded_file = [row.replace('\r', '') for row in decoded_file]
            decoded_file = [row.replace('\"', '') for row in decoded_file]
            decoded_file = decoded_file[:-1]
            SNPArray.multiprocess_text(decoded_file)

    def excel_file(self):
        decoded_file = []
        workbook = xlrd.open_workbook(self)
        first_sheet = workbook.sheet_by_index(0)
        for rownum in range(first_sheet.nrows):
            rsid = str(first_sheet.cell(rownum, 0))
            rsid = rsid.replace("text:", '')
            chromosome = str(first_sheet.cell(rownum, 1))
            chromosome = chromosome.split(".")[0]
            chromosome = chromosome.replace("number:", '')
            position = str(first_sheet.cell(rownum, 2))
            position = position.split(".")[0]
            position = position.replace("number:", '')
            alleles = str(first_sheet.cell(rownum, 3))
            alleles = alleles.replace("text:", '')
            row = rsid + "\t" + str(chromosome) + "\t" + str(position) + "\t" + alleles
            row = row.replace("\'", '')
            decoded_file.append(row)
        SNPArray.multiprocess_text(decoded_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(sys.argv[1:])
    parser.add_argument("-g", "--genome", help="reference genome build, \
    default = 37", default=37)
    parser.add_argument("-o", "--output", help="output directory", default="./out")
    parser.add_argument("-i", "--input", help="input directory", default="./")
    parser.add_argument("-t", "--threads", help="number of threads", type=int, default=1)
    # parser.add_argument("-f", "--format", help="output format \
    # default = vcf: VCF")
    arguments = parser.parse_args()
    print(arguments)
    for file in os.listdir(arguments.input):
        if os.path.isdir(file):
            pass
        elif file.startswith("."):
            pass
        elif "exome" in file:
            pass
        else:
            file_name = arguments.input + "/" + file
            file_identifier = file.split("/")[-1].split("_")
            user = file_identifier[0]
            file = file_identifier[1]
            out_dir_file = arguments.output + "/" + user + "_" + file + ".txt"
            if "text" in SNPArray.extract_file_type(file_name):
                SNPArray.text_file(file_name)
                print(file_name, "text")
            elif "PDF" in SNPArray.extract_file_type(file_name):
                print(file_name, "PDF")
            elif "gzip" in SNPArray.extract_file_type(file_name):
                SNPArray.gzip_file(file_name)
                print(file_name, "gzip")
            elif "Zip" in SNPArray.extract_file_type(file_name):
                SNPArray.zip_file(file_name)
                print(file_name, "zip")
            elif "Excel" in SNPArray.extract_file_type(file_name):
                SNPArray.excel_file(file_name)
                print(file_name, "Excel")
            else:
                SNPArray.text_file(file_name)
                print(file_name, "probably text")

end = time.time()

print(end - start)
