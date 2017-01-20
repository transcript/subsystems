#!/usr/lib/python2.6

# Subsystems_simplifier.py
# created 12/22/16, Sam Westreich

# Purpose: The subsystems.complex database is not organized well for searches.  This script tries to make it a little more useful as an annotation database.

import sys, re

if len(sys.argv) != 2:
	sys.exit("Need to specify database file as ARGV1.")

infile = open(sys.argv[1], "r")
outfile = open(sys.argv[1] + ".modified", "w")

line_counter = 0
prev_line_protein = True

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
	
	# The following are just for debug purposes:
	elif line[0] == ">":
		if prev_line_protein == True:
			if line_counter == 1:
				outfile.write(line)
			else:
				outfile.write("\n" + line)
			prev_line_protein = False
			continue
		else:
			continue

	elif len(re.sub("[A-Zx]", "", line.strip())) == 0:
		outfile.write(line.strip())
		prev_line_protein = True
		continue

	else:
		continue
