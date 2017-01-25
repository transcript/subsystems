# subsystems code
Code for making bioinformatics work with the SEED subsystems database a little easier.

Location for obtaining the raw files - the FTP Seed site, Subsystems folder: [ftp://ftp.theseed.org/subsystems/](ftp://ftp.theseed.org/subsystems/)

For a full write-up of the initial reasons behind this code, check out the blog post here: [http://www.metatranscriptomics.com/2017/01/working-with-subsystems-functional.html](http://www.metatranscriptomics.com/2017/01/working-with-subsystems-functional.html)

### contents
* Subsystems_simplifier.py - takes the "subsystems.complex" big file and makes it into a bioinformatics-friendly layout (FASTA, suitable to be used by annnotation algorithms like BLAST and DIAMOND as a database)
* FIG_extractor.py - takes the "subsystems.complex" big file and extracts Fig IDs and their associated functions (level 4 in the Subsystems hierarchy, the lowest level)
* fig_swapper.py - takes four files - the output of FIG_extractor, a results file with Fig IDs, the "subsystems2role" file, and "subsys.txt" file - and adds both function names and hierarchy (when it can be found) to each Fig ID in the results file.
* subsys_db_rebuilder - performs all of the above steps to create one large index file with all combined information.  Best for creating a single custom database that can be searched later.

### Usage - creating a single database file with all information
**Program used:** 	subsys_db_rebuilder.py    
**Files needed:**	subsystems.complex    
			subsys2role    
			subsys2peg    
			subsys.txt


**Command:**    
    `python2.7 subsys_db_rebuilder.py subsystems.complex subsys2role subsys2peg subsys.txt`

Note that the four input files need to be in this specific order for the program to work.

**Output:** Two files:    

* subsystems.complex.merged - this large file, in FASTA format, contains all protein sequences from the Subsystems database.  The header contains - tab separated:
	* The Fig ID
	* The specific function (level 4 hierarchy)
	* Level 3 hierarchy
	* Level 2 hierarchy
	* Level 1 hierarchy (top level of Subsystems)
	* Other IDs (GI accessions, GO terms, etc.)
* subsystems.complex.no_hierarchy - not all Subsystems sequences have hierarchy information.  These "NO HIERARCHY" sequences are carried over into subsystems.complex.merged, but are also printed in this file, in the same format as above.

### Usage - getting hierarchy for specific Fig IDs
Perhaps you don't care about rebuilding the entire database, and just want to know the hierarchy for your list of Fig IDs.  In that case, the following program should help.

**Program used:**	fig_swapper.py   
**Files needed:**	subsystems2role    
			subsystems2peg    
			subsys.txt    
			tab-separated results file, with Fig IDs in column 3

**Command:**    
    `python2.7 fig_swapper.pysubsystems2peg results_file subsystems2role subsys.txt`

**Output:**  The input file with ".converted" as a suffix.  This file should contain the original 3 columns, with additional hierarchy information added after the Fig ID as extra columns.  These columns go in reverse hierarchy; level 4, level 3, level 2, and level 1 as the right-most column.
