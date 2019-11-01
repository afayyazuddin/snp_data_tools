The openSNPs project provides one of the few completely open resources of human genetic data along with self-reported phenotype data that can be used with statistical genetics tools. However, since both types of data are provided by volunteers there are a variety of data cleaning problems that have to be addressed before the data can be used for any inference. The particular challenges I have identified are as follows:

Even though the genotype files are labeled as .txt files, many of them are not text files. They are actually in several different formats including Excel, zip, and gzip.
The data come from several different direct to consumer platforms such as ***23 and Me***, ***Ancestry***, and ***Family Tree DNA*** and thus have to be standardized to one format.
The genetic coordinates are to different builds of the human genome and many times the build version is not provided in the header.

While the steps listed above are of primary importance and must be addressed before any work can be done with the data, there are secondary cleaning tasks which would make the data easier to interpret in the long run. Some of these issues are listed below:

Many of the SNPs are re-encoded with proprietary identifiers rather than rsid numbers.
The SNP arrays being used change over time so the same SNPs are not represented in each genotypes.

I have broken this problem into several steps. To convert all files to text and standardize formats I have written a program called snp_data_tools.py which will identify the file type using the ```magic``` module, strip the headers, and standardize all files to the 23 and Me format. When the genome build is provided in the header, it will extract that information and add it to the file name. I am still working on extracting the build directly from the genome coordinates.

Next steps that I haven’t implemented yet involve using the VCF format instead of ***23 and Me*** and then using a liftover program to convert it to the genome build of choice. I also plan to convert the proprietary encoded SNPs to rsids. So far I have identified more than 88000 such SNPs in the ***23 and Me*** data and smaller numbers in the ***FT-DNA*** (127) and ***Ancestry*** (12) datasets. I have mapped the coordinates for a handful of these SNPs using the UCSC SNP database and all of the ones I tested have corresponding rsids. On the phenotypic data side the main data cleaning task is to standardize formats because the same trait, e.g. blood type, is represented multiple times and the same phenotypic variant is encoded in multiple ways.
