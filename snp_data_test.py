import unittest
from snp_data_tools import SNP, SNPArray

with open("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test.txt", 'r') as infile:
    input_file = infile.readlines()


def snp_data(snp):
    """Return tuple of chromosome data"""
    return (snp.rsid, snp.chromosome, snp.position, snp.allele1, snp.allele2)


class SNPTests(unittest.TestCase):

    def test_twentythreeandme_conv(self):
        """Test conversion of snp object from 23andMe"""
        snp = SNP.convert("rs4477212\t1\t82154\tAA")
        expected = ("rs4477212", "1", "82154", "A", "A")
        self.assertEqual(snp_data(snp), expected)

    def test_ancestry_conv(self):
        """Test conversion of snp object from ancestry"""
        snp = SNP.convert("rs4477212\t23\t82154\tA\tA")
        expected = ("rs4477212", "X", "82154", "A", "A")
        self.assertEqual(snp_data(snp), expected)

    def test_ftdna_conv(self):
        """Test conversion of snp object from ft-dna"""
        snp = SNP.convert('"rs4477212","1","82154","AA"')
        expected = ("rs4477212", "1", "82154", "A", "A")
        self.assertEqual(snp_data(snp), expected)


class zip_file_Tests(unittest.TestCase):
    pass


class SNPArrayTests(unittest.TestCase):

    def test_23andMe_file_autosome(self):
        """Test conversion of 23andMe file for autosome"""
        with open("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test.txt", 'r') as infile:
            input_file = infile.readlines()
            print(input_file)
            snp_array = [SNPArray.convert_text(row) for row in input_file if not (row.startswith("RSID") or row.startswith("#") or row.startswith("rsid") or not row.strip())]
        expected = "rs4477212" + "\t" + "1" + "\t" + "82154" + "\t" + "AA"
        print(snp_array[0])
        print(expected)
        self.assertEqual(snp_array[0], expected)

    def test_23andMe_file_MT(self):
        """Test conversion of 23andMe file for MT chromosome"""
        with open("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test.txt", 'r') as infile:
            input_file = infile.readlines()
            snp_array = [SNPArray.convert_text(row) for row in input_file if not (row.startswith("RSID") or row.startswith("#") or row.startswith("rsid") or not row.strip())]
        expected = ("i702862" + "\t" + "MT" + "\t" + "16312" + "\t" + "A")
        self.assertEqual(snp_array[5], expected)

    '''def test_23andMe_file_autosome(self):
        """Test conversion of 23andMe file for autosome"""
        # with open("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test.txt", 'r') as infile:
        #    input_file = infile.readlines()
        snp_array = SNPArray.make_snp_file(input_file)
        expected = ("rs4477212", "1", "82154", "A", "A")
        self.assertEqual(snp_data(snp_array[0]), expected)

    def test_23andMe_file_MT(self):
        """Test conversion of 23andMe file for MT chromosome"""
        # with open("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test.txt", 'r') as infile:
        #    input_file = infile.readlines()
        snp_array = SNPArray.make_snp_file(input_file)
        expected = ("i702862", "MT", "16312", "A", "")
        self.assertEqual(snp_data(snp_array[5]), expected)'''

    '''def test_genome_version_in_metadata(self):
        """Test pulling out genome version from file metadata"""
        genome_build = SNPArray.get_genome_version_from_metadata(input_file)
        expected = '37'
        self.assertEqual(genome_build, expected)'''

    def test_genome_version_from_coords_hg19(self):
        """Test getting genome version from coordinates"""
        first_snp = ["rs4477212\t1\t82154\tAA"]
        # with open("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test_coords.txt", 'r') as infile:
        #    test_coords = infile.readlines()
        genome_build = SNPArray.get_genome_version_from_coordinates(first_snp)
        expected = '37'
        self.assertEqual(genome_build, expected)

    def test_genome_version_from_coords_hg18(self):
        """Test getting genome version from coordinates"""
        first_snp = ["rs3094315\t1\t742429\tAG"]
        # with open("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test_coords.txt", 'r') as infile:
        #    test_coords = infile.readlines()
        genome_build = SNPArray.get_genome_version_from_coordinates(first_snp)
        expected = '36'
        self.assertEqual(genome_build, expected)


if __name__ == "__main__":
    unittest.main()
