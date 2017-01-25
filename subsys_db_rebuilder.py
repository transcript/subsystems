#!/usr/lib/python2.7

# subsys_db_rebuilder.py

# purpose: take the Subsystems starting files and create a DIAMOND-searchable database that can return full hierarchy (when available) instead of just Fig IDs.

import sys, time, re

print "Usage: subsys_db_rebuilder.py subsystems.complex subsystems2role subsystems2peg subsys.txt"

try:
	subsys_complex_name = sys.argv[1]
	subsys2role_name = sys.argv[2]
	subsys2peg_name = sys.argv[3]
	subsys_hier = sys.argv[4]
except IndexError:
	sys.exit("Match the usage statement")

# Step 1: get a database of FIG IDs to level 3 and 4 protein functions
infile = open(subsys2peg_name, "r")

line_counter = 0
peg_dic = {}

for line in infile:
	splitline = line.strip().split("\t")
	peg_dic[splitline[2]] = str(splitline[1] + "\t" + splitline[0])
	line_counter += 1

infile.close()

print "Step 1 complete."
print str(line_counter) + " Fig IDs read into dictionary."

# Step 2: connect the level 3 protein functions to levels 1 and 2
infile = open(subsys2role_name, "r")

line_counter = 0
role_dic = {}

for line in infile:
	line_counter += 1
	splitline = line.strip().split("\t")
	role_dic[splitline[0]] = str(splitline[1] + "\t" + splitline[2])

infile.close()

print "Step 2 complete."
print str(line_counter) + " lines from subsystems2role read in."

# Step 3: adding these level 1 and 2 functions to the dictionary in memory
for entry in peg_dic.keys():
	splitvalue = peg_dic[entry].split("\t")
	if len(splitvalue) != 4:
		peg_dic[entry] = splitvalue[0] + "\t" + splitvalue[1] + "\t" + role_dic[splitvalue[1]]

print "Step 3 complete."
print str(line_counter) + " lines from subsystems2role added to dictionary."

# Step 4: Now, we're going to read through the subsystems.complex file and restructure it, using the Fig IDs in that file to add in the hierarchy.
infile = open(subsys_complex_name, "r")
outfile = open(subsys_complex_name + ".merged", "w")
no_hier_file = open(subsys_complex_name + ".no_hierarchy", "w")

line_counter = 0
written_counter = 0
no_hier_match = 0
prev_line_protein = True
no_hier = False

for line in infile:
	line_counter += 1
	if line_counter % 100000 == 0:
		print str(line_counter)[:-3] + "k lines processed so far."
	if re.match("\d", line[0]):
		continue							# removes lines starting with numbers
	elif re.match("^fig", line):
		continue							# removes lines starting with "fig"
	elif re.match("^//", line):
		continue							# removes the double slashes, //
	elif "All" in line:
		continue							# removes where it says "All" for some reason
	elif line[0] == "#":
		continue							# removes the ######## dividers
	
	# This part catches the FASTA header for each protein sequence
	elif line[0:4] == ">fig":
		no_hier = False
		if prev_line_protein == True:
			if written_counter == 0:
				written_counter += 1
				splitline = line.split(" ", 1)
				fig_id = splitline[0][1:]
				
				try:
					out_line = ">" + fig_id + "\t" + peg_dic[fig_id] + "\t" + splitline[1]
				except KeyError:
					out_line = ">" + fig_id + "\tNO HIERARCHY\t" + splitline[1]
					no_hier_match += 1
				outfile.write(out_line)
				
			else:
				#outfile.write("\n" + line)
				splitline = line.split(" ", 1)
				fig_id = splitline[0][1:]
				
				try:
					out_line = ">" + fig_id + "\t" + peg_dic[fig_id] + "\t" + splitline[1]
				except KeyError:
					try:
						out_line = ">" + fig_id + "\tNO HIERARCHY\t" + splitline[1]
						no_hier_match += 1
						no_hier_file.write(out_line)
						no_hier = True
					except IndexError:
						print line
						print str(line_counter)
						sys.exit ("Hit an index error")
				outfile.write("\n" + out_line)

			prev_line_protein = False
			continue
		else:
			continue

	# this part catches the actual protein sequence
	elif len(re.sub("[A-Zx]", "", line.strip())) == 0:
		outfile.write(line.strip())
		prev_line_protein = True
		
		if no_hier == True:
			no_hier_file.write(line)
			
		continue

	else:
		continue

infile.close()
outfile.close()
no_hier_file.close()

print "Full test complete: " + str(line_counter) + " lines of the subsystems.complex file processed."
print "Number of sequences with no associated hierarchy: " + str(no_hier_match)