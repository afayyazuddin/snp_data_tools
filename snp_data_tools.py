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
from pyliftover import LiftOver
import time
# import itertools
# from subprocess import Popen, PIPE
# from pathlib import Path
# import pysam

parser = argparse.ArgumentParser(sys.argv[1:])
parser.add_argument("-g", "--genome",
                    help="reference genome build, default = 37",
                    default=37)
parser.add_argument("-o", "--output",
                    help="output directory",
                    default="./out")
parser.add_argument("-i", "--input",
                    help="input directory",
                    default="./")
parser.add_argument("-t", "--threads",
                    help="number of threads",
                    type=int, default=1)
parser.add_argument("-f", "--format",
                    help="output format, default is 23andMe",
                    default="23andMe",
                    choices=['23andMe', 'bed'])

# parser.add_argument("-f", "--fasta", help="location of fasta files \
# default = vcf: VCF")

start = time.time()
with open("genome_build_coords.txt", 'r') as infile:
    coords = infile.readlines()[0]
    coords_dict = eval(coords)


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
        # convert Ancestry coding for X to 23andMe
        if chromosome == "23":
            chromosome = "X"
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
        return "{} at chromosome {} position {} with \
        variants {} and {}".format(self.rsid,
                                   self.chromosome,
                                   self.position,
                                   self.allele1,
                                   self.allele2)

    def __repr__(self):
        return "SNP (rsid={}, chromosome={}, position={}, \
        allele1={}, allele2={})".format(self.rsid,
                                        self.chromosome,
                                        self.position,
                                        self.allele1,
                                        self.allele2)


class SNPArray():
    def __init__(self, snps, user, opensnp_file_id, vendor, genome):
        self.snps = snps
        self.user = user
        self.opensnp_file_id = opensnp_file_id
        self.vendor = vendor
        self.genome = genome  # genome

    # allow indexing of SNPArray object
    def __getitem__(self, i):
        return self.snps[i]

    def __iter__(self):
        return self.snps

    def __repr__(self):
        return "{}".format(self.snps)

    def populate_SNPArray_metadata(self):
        directory = self[0]
        file = self[1]
        file_name = directory + "/" + file
        vendor = file.split(".")[-2]
        file_identifier = file.split("/")[-1].split("_")
        user = file_identifier[0]
        opensnp_file_id = file_identifier[1]
        print(file_name, vendor)
        if "text" in SNPArray.extract_file_type(file_name):
            snps = SNPArray.text_file(file_name)
            print(file_name, "text")
        elif "PDF" in SNPArray.extract_file_type(file_name):
            print(file_name, "PDF")
        elif "gzip" in SNPArray.extract_file_type(file_name):
            snps = SNPArray.gzip_file(file_name)
            print(file_name, "gzip")
        elif "Zip" in SNPArray.extract_file_type(file_name):
            snps = SNPArray.zip_file(file_name)
            print(file_name, "zip")
        elif "Excel" in SNPArray.extract_file_type(file_name):
            snps = SNPArray.excel_file(file_name)
            print(file_name, "Excel")
        else:
            snps = SNPArray.text_file(file_name)
            print(file_name, "unknown")

        genome = SNPArray.get_genome_version_from_coordinates(snps)
        print(snps[1])

        return SNPArray(snps, user, opensnp_file_id, vendor, genome)

    def extract_file_type(self):
        with magic.Magic() as m:
            # for filename in os.listdir(dir):
            #    file = dir+filename
            return m.id_filename(self)

    '''def get_genome_version_from_metadata(self):
        # check for genome build in the first 25 lines
        for row in itertools.islice(self, 25):
            result = re.search('(?<=build )(..)', row)
            if result is not None:
                genome_build = result.group(1)
                break
        return genome_build'''

    def get_genome_version_from_coordinates(self):
        test_snp = SNP.convert(self[0])
        snp_coords = ("chr"+str(test_snp.chromosome), int(test_snp.position)-1)

        test_coords_18 = coords_dict.get('hg18').get(test_snp.rsid)
        test_coords_19 = coords_dict.get('hg19').get(test_snp.rsid)

        if snp_coords == test_coords_18:
            genome_build = "36"
        elif snp_coords == test_coords_19:
            genome_build = "37"
        else:
            genome_build = "unknown"

        return genome_build

    def change_genome_version(self):
        pass

    def convert_text(self):
        SNP_row = SNP.convert(self)
        return (SNP_row.rsid + "\t"
                + SNP_row.chromosome + "\t"
                + SNP_row.position
                + "\t"
                + SNP_row.allele1 + SNP_row.allele2)

    def multiprocess_text(self):
        '''global genome_build
        if vendor == ("23andme" or "ancestry") and
                      type(self) == '_io.TextIOWrapper':
            # Deal with cases where the file is already read into a list
            if self.readline().startswith("#"):
                # Deal with cases where file doesn't have comments
                genome_build = SNPArray.get_genome_version_from_metadata(self)
            else:
                genome_build = ""
        else:
            genome_build = ""'''
        p = mp.Pool(arguments.threads)
        result = p.map(SNPArray.convert_text, [row for row in self if not
                                               (row.startswith("RSID") or
                                                row.startswith("#") or
                                                row.startswith("rsid") or
                                                not row.strip())])
        # write_file(result)
        return(result)
        ''' ignore lines that are empty, are comments or are headers'''

    def text_file(self):
        with open(self, 'r') as infile:
            snps = SNPArray.multiprocess_text(infile)
        return(snps)

    def gzip_file(self):
        '''using zcat to read gzip files. May not work in non-unix systems
        f = Popen(['zcat', self], stdout=PIPE)
        decoded_file = [line for line in f.stdout]
        SNPArray.multiprocess_text(decoded_file)'''

        # The following code fails for some gzipped files without .gz extension
        with gzip.open(self, 'r') as infile:
            all_data = infile.read().split()
            decoded_file = [row.decode("utf-8")for row in all_data]
            snps = SNPArray.multiprocess_text(decoded_file)
            return(snps)

    def zip_file(self):
        with ZipFile(self, 'r') as zip:
            name = zip.namelist()[0]
            print(name)
            decoded_file = zip.read(name).decode("utf-8")
            decoded_file = decoded_file.split("\n")
            decoded_file = [row.replace('\r', '') for row in decoded_file]
            decoded_file = [row.replace('\"', '') for row in decoded_file]
            decoded_file = decoded_file[:-1]
            snps = SNPArray.multiprocess_text(decoded_file)
            return(snps)

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
            row = rsid + "\t"
            + str(chromosome) + "\t"
            + str(position)
            + "\t" + alleles
            row = row.replace("\'", '')
            decoded_file.append(row)
        snps = SNPArray.multiprocess_text(decoded_file)
        return(snps)

    def to_vcf(self):
        pass

    def write_file(self):
        print(self.user)
        # print(self.snps)
        # out_dir_file = arguments.output + "/" + user + "_" + file + "gen"
        # + genome_build + ".txt"
        out_dir_file = arguments.output + "/"
        + self.user + "_"
        + self.opensnp_file_id + "_"
        + self.vendor + "_"
        + self.genome + ".txt"
        with open(out_dir_file, 'w') as outfile:
            for row in self.snps:
                csv_writer = csv.writer(outfile, delimiter="\t")
                csv_writer.writerows([row.split("\t")])


if __name__ == "__main__":
    arguments = parser.parse_args()
    print(arguments)
    for file in os.listdir(arguments.input):
        if os.path.isdir(file):
            pass
        elif not file.startswith("user"):
            pass
        elif "exome" in file:
            pass
        elif "IYG" in file:
            pass
        else:
            SNPArray.populate_SNPArray_metadata([arguments.input, file])
            # f = SNPArray.populate_SNPArray_metadata([arguments.input, file])
            # f.write_file()

end = time.time()

print(end - start)
