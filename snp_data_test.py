import unittest
from snp_data_tools import SNP, SNPArray


def snp_data(snp):
    """Return tuple of Point data for comparison """
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

    def test_23andMe_file(self):
        """Test conversion of 23andMe file"""
        snp_array = SNPArray.make_snp_file("/Users/amir/Documents/Analysis/snp_data_tools/23andme_test.txt")
        expected = ("rs4477212", "1", "82154", "A", "A")
        self.assertEqual(snp_data(snp_array[0]), expected)


if __name__ == "__main__":
    unittest.main()
