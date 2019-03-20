import unittest
from snp_data_tools import SNP, SNPArray, GenomeVersion


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
        snp = SNP.convert("rs4477212\t1\t82154\tA\tA")
        expected = ("rs4477212", "1", "82154", "A", "A")
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
        snp_array = SNPArray.make_snp_file("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test.txt")
        expected = ("rs4477212", "1", "82154", "A", "A")
        self.assertEqual(snp_data(snp_array[0]), expected)

    def test_23andMe_file_MT(self):
        """Test conversion of 23andMe file for MT chromosome"""
        snp_array = SNPArray.make_snp_file("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test.txt")
        expected = ("i702862", "MT", "16312", "A", "")
        self.assertEqual(snp_data(snp_array[5]), expected)


class GenomeVersionTests(unittest.TestCase):

    def test_genome_version_in_metadata(self):
        """Test pulling out genome version from file metadata"""
        genome_build = GenomeVersion.get_genome_version_from_metadata("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test.txt")
        expected = '37'
        self.assertEqual(genome_build, expected)

    def test_genome_version_from_coords(self):
        """Test getting genome version from coordinates"""
        genome_build = GenomeVersion.get_genome_version_from_coordinates("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test_coords.txt")
        expected = '37'
        self.assertEqual(genome_build, expected)


if __name__ == "__main__":
    unittest.main()
