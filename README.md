# subsystems code
Code for making bioinformatics work with the SEED subsystems database a little easier.

Useful link - the FTP Seed site, Subsystems folder: ftp://ftp.theseed.org/subsystems/

For a full write-up, check out the blog post here: http://www.metatranscriptomics.com/2017/01/working-with-subsystems-functional.html

## contents
* Subsystems_simplifier.py - takes the "subsystems.complex" big file and makes it into a bioinformatics-friendly layout (FASTA, suitable to be used by annnotation algorithms like BLAST and DIAMOND as a database)
* FIG_extractor.py - takes the "subsystems.complex" big file and extracts Fig IDs and their associated functions (level 4 in the Subsystems hierarchy, the lowest level)
* fig_swapper.py - takes four files - the output of FIG_extractor, a results file with Fig IDs, the "subsystems2role" file, and "subsys.txt" file - and adds both function names and hierarchy (when it can be found) to each Fig ID in the results file.

More to come.

